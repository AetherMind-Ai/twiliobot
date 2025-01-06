from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
import os

app = Flask(__name__)


# Use environment variables for credentials (Vercel or locally)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-pro')

@app.route("/sms", methods=["POST"])
def incoming_sms():
    """Handles incoming WhatsApp messages."""
    message_body = request.form.get("Body")
    from_number = request.form.get("From")

    # Respond with Gemini's response
    gemini_response = get_gemini_response(message_body)

    resp = MessagingResponse()
    resp.message(gemini_response)

    return str(resp)

def get_gemini_response(prompt):
    """Gets a response from the Gemini API."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error processing your request: {e}"

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)