# WhatsApp Reminder Bot with Gemini AI

A WhatsApp bot that uses Google's Gemini AI to understand and set reminders, storing them in Google Sheets and sending notifications at appropriate times.

## Features

- Natural language processing for setting reminders
- Smart date/time understanding (today, tomorrow, next week, etc.)
- Google Sheets integration for storing reminders
- Automated reminders at:
  - 15 minutes before the event
  - 5 minutes before the event
  - At the event time
- Interactive conversation for missing information

## Setup Instructions

1. **Environment Setup**
   ```bash
   pip install -r requirements.txt
   ```

2. **Google Cloud Setup**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable Google Sheets API and Google Drive API
   - Create a service account and download the credentials JSON file
   - Save the credentials file as `credentials.json` in the project root

3. **Google Sheets Setup**
   - Create a new Google Sheet named "Reminders"
   - Share the sheet with the service account email
   - Create these three columns in the first row:
     ```
     A1: Event Name
     B1: Date
     C1: Time
     ```
   - Format the columns:
     - Select all cells
     - Click "Format" > "Text wrapping" > "Wrap"
     - Click "Format" > "Alignment" > "Center"

4. **Environment Variables**
   Create a `.env` file with:
   ```
   WA_TOKEN=your_whatsapp_token
   GEN_API=your_gemini_api_key
   PHONE_ID=your_phone_id
   PHONE_NUMBER=your_phone_number
   ```

5. **WhatsApp Business API Setup**
   - Set up a WhatsApp Business API account
   - Configure the webhook URL to point to your server
   - Set the verify token to "BOT"

## Usage

Send messages to the bot in natural language, for example:
- "Remind me to call John tomorrow at 3pm"
- "Set a reminder for my meeting next Monday at 10am"
- "I have a doctor's appointment on June 15th at 2:30pm"

The bot will:
1. Understand your message
2. Ask for any missing information
3. Confirm the details
4. Save the reminder
5. Send notifications at appropriate times

## Example Conversations

User: "Remind me to call John tomorrow at 3pm"
Bot: "✅ Reminder set for 'Call John' on [tomorrow's date] at 3:00 PM"

User: "Set a meeting reminder"
Bot: "I need a few more details. What is the meeting about, and when is it scheduled?"

## Error Handling

The bot will:
- Ask for clarification if information is missing
- Handle various date/time formats
- Send error messages if something goes wrong
- Confirm successful reminder creation

## Security

- All sensitive information is stored in environment variables
- Google Sheets access is secured through service account authentication
- WhatsApp messages are processed securely through the official API

## Contributing

Feel free to submit issues and enhancement requests!

#### Please give a ⭐ if you like it.

### Follow the video tutorial to set up the bot 🤩👇

### ⚠️ Don't clone. It won't work in Local environment. Follow the steps in the video.

# Whatsapp_Gemini_Bot
**Get Google Gemini AI On WhatsApp, without port forwarding. An always online WhatsApp bot by creating a flask server on Vercel.**

## Complete tutorial video:

[![Watch the video](https://img.youtube.com/vi/zT0YTfizzxM/0.jpg)](https://youtu.be/zT0YTfizzxM)


## Image Examples:

<img src="images/Screenshot_2024-05-07-17-17-07-249_com.whatsapp.jpg" alt="working1" width="300" height=750>

<img src ="images/Screenshot_2024-05-25-22-02-01-088_com.whatsapp.jpg" alt="working2"  width="300" height=750>

## 👆Bot can respond to images and audio

<img src="images/Screenshot_20240528_224908_WhatsApp.jpg" alt="working3"  width="300" height=750>

## Bot can respond to pdf also.
