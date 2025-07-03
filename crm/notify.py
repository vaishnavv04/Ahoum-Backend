import requests
import os
from dotenv import load_dotenv
load_dotenv()

CRM_WEBHOOK_URL = os.getenv("CRM_WEBHOOK_URL")

def notify_crm(data):
    try:
        response = requests.post(CRM_WEBHOOK_URL, json=data, timeout=5)
        print(f"CRM Notified: {response.status_code}")
    except Exception as e:
        print(f"CRM Notification Failed: {e}")