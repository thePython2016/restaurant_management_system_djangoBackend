import requests
import json
import os

class MamboSMSService:
    def __init__(self):
        self.base_url = os.getenv('MAMBO_SMS_BASE_URL', 'https://mambosms.co.tz')
        self.api_key = os.getenv('MAMBO_SMS_API_KEY')
        
    def send_sms(self, sender_id, message, mobile):
        """
        Send SMS via Mambo SMS API
        """
        if not self.api_key:
            return {
                'success': False,
                'error': 'API key not configured'
            }
            
        url = f"{self.base_url}/api/v1/sms/single"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        payload = {
            "sender_id": sender_id,
            "message": message,
            "mobile": mobile  # Format: 0713XXXXXX
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'data': response.json() if response.content else {},
                'error': None if response.status_code == 200 else f"HTTP {response.status_code}"
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Request failed: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }