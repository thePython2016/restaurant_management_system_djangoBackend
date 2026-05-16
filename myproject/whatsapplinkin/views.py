from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

WHATSAPP_API_URL = "https://graph.facebook.com/v20.0"
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

@csrf_exempt
def send_whatsapp_message(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        user_number = data.get("phone_number")  # customer number in international format
        message = data.get("message", "Hello from Django + WhatsApp API!")

        url = f"{WHATSAPP_API_URL}/{PHONE_NUMBER_ID}/messages"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": user_number,
            "type": "text",
            "text": {"body": message}
        }

        response = requests.post(url, headers=headers, json=payload)

        return JsonResponse(response.json(), safe=False)

    return JsonResponse({"error": "Invalid request"}, status=400)
