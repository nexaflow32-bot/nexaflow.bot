from flask import Flask, request
import anthropic
from twilio.rest import Client
import os

app = Flask(__name__)

claude = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
twilio_client = Client(os.environ.get("TWILIO_ACCOUNT_SID"), os.environ.get("TWILIO_AUTH_TOKEN"))

@app.route("/whatsapp/webhook", methods=["POST"])
def whatsapp():
    incoming_msg = request.form.get("Body")
    sender = request.form.get("From")
    
    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system="You are NexaFlow.ai's AI sales assistant based in Accra Ghana. NexaFlow is an AI automation agency founded by Gerald. Help businesses automate using WhatsApp chatbots. Pricing: GHS 500 setup, GHS 150 per month. Book demos by asking preferred day and time. Be friendly and confident.",
        messages=[{"role": "user", "content": incoming_msg}]
    )
    
    reply = response.content[0].text
    twilio_client.messages.create(
        from_="whatsapp:+14155238886",
        to=sender,
        body=reply
    )
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
