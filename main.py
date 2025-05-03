import google.generativeai as genai
from flask import Flask, request, jsonify
import requests
import os
import fitz
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import schedule
import time
from datetime import datetime, timedelta
from dateutil import parser
import threading

# Initialize Flask app
app = Flask(__name__)

# Environment variables
wa_token = os.environ.get("WA_TOKEN")
genai.configure(api_key=os.environ.get("GEN_API"))
phone_id = os.environ.get("PHONE_ID")
phone = os.environ.get("PHONE_NUMBER")
name = "Your name or nickname"
bot_name = "Reminder Bot"
model_name = "gemini-1.5-flash-latest"

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open('1rl5SfSA0OtQoLMmr9ASfAgNrREdj1TUeFlzeHH5XWM').sheet1
# Initialize Gemini model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name=model_name,
                            generation_config=generation_config,
                            safety_settings=safety_settings)

# Initialize conversation with specific prompt for reminder bot
convo = model.start_chat(history=[])
convo.send_message(f'''You are a reminder bot assistant. Your task is to:
1. Extract event details from user messages including:
   - Event name
   - Date (handle relative dates like "today", "tomorrow", "next week")
   - Time
2. If any information is missing, ask the user for clarification
3. Format your responses to be clear and concise
4. Always confirm the details before saving
5. Use natural language to interact with users''')

def send(answer):
    url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
    headers = {
        'Authorization': f'Bearer {wa_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "messaging_product": "whatsapp",
        "to": f"{phone}",
        "type": "text",
        "text": {"body": f"{answer}"},
    }
    response = requests.post(url, headers=headers, json=data)
    return response

def parse_date_time(text):
    try:
        # Try to parse the date and time
        dt = parser.parse(text)
        return dt
    except:
        return None

def save_reminder(event_name, date, time):
    # Add reminder to Google Sheet
    row = [event_name, date, time]
    sheet.append_row(row)
    return True

def check_reminders():
    now = datetime.now()
    # Get all reminders from sheet
    reminders = sheet.get_all_records()
    
    for reminder in reminders:
        reminder_time = parser.parse(f"{reminder['Date']} {reminder['Time']}")
        
        # Check if reminder is due in 15 minutes
        if (reminder_time - now).total_seconds() <= 900 and (reminder_time - now).total_seconds() > 0:
            send(f"🔔 Reminder: {reminder['Event Name']} is in 15 minutes!")
        
        # Check if reminder is due in 5 minutes
        elif (reminder_time - now).total_seconds() <= 300 and (reminder_time - now).total_seconds() > 0:
            send(f"🔔 Reminder: {reminder['Event Name']} is in 5 minutes!")
        
        # Check if reminder is due now
        elif (reminder_time - now).total_seconds() <= 0:
            send(f"🔔 Reminder: {reminder['Event Name']} is now!")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Schedule reminder checks every minute
schedule.every(1).minutes.do(check_reminders)

# Start scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

@app.route("/", methods=["GET", "POST"])
def index():
    return "Reminder Bot"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == "BOT":
            return challenge, 200
        else:
            return "Failed", 403
    elif request.method == "POST":
        try:
            data = request.get_json()["entry"][0]["changes"][0]["value"]["messages"][0]
            if data["type"] == "text":
                prompt = data["text"]["body"]
                
                # Process the message with Gemini
                convo.send_message(prompt)
                response = convo.last.text
                
                # Check if response contains all required information
                if "Event Name:" in response and "Date:" in response and "Time:" in response:
                    # Extract information from response
                    event_name = response.split("Event Name:")[1].split("\n")[0].strip()
                    date = response.split("Date:")[1].split("\n")[0].strip()
                    time = response.split("Time:")[1].split("\n")[0].strip()
                    
                    # Save reminder
                    save_reminder(event_name, date, time)
                    send(f"✅ Reminder set for {event_name} on {date} at {time}")
                else:
                    # Ask for missing information
                    send(response)
            else:
                send("Please send text messages only for setting reminders.")
        except Exception as e:
            send(f"Sorry, I encountered an error: {str(e)}")
        return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=8000)
