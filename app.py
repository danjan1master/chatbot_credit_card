from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # 🔄 Load environment variables

app = Flask(__name__)
CORS(app)

# 🔐 Get your HubSpot token from .env
HUBSPOT_TOKEN = os.getenv("HUBSPOT_API_TOKEN")

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json

    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    income = data.get('income')
    preference = data.get('preference')  # Card recommendation

    print("✅ New Lead Received:")
    print(f"Name: {name}, Email: {email}, Age: {age}, Income: {income}, Preference: {preference}")

    # 🔄 Push data to HubSpot CRM
    try:
        url = "https://api.hubapi.com/crm/v3/objects/contacts"
        headers = {
            "Authorization": f"Bearer {HUBSPOT_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "properties": {
                "email": email,
                "firstname": name,
                "age": age,
                "income": income,
                "card_recommendation": preference,
                "source": "Chatbot",
                "followup_status": "Pending"
            }
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 201:
            print("✅ Contact successfully added to HubSpot.")
        elif response.status_code == 409:
            print("⚠️ Contact already exists in HubSpot.")
        else:
            print("❌ HubSpot error:", response.text)

    except Exception as e:
        print("❌ Error pushing to HubSpot:", e)

    return jsonify({
        'message': f'Thank you {name}, your card recommendation has been processed.'
    })

if __name__ == '__main__':
    app.run(debug=True)
