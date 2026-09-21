import os
import requests
from dotenv import load_dotenv

load_dotenv()

PUSHOVER_API_URL = "https://api.pushover.net/1/messages.json"


def send_pushover_notification(
    message,
    title="NovaTech Enterprise Assistant"
):

    user_key = os.getenv("PUSHOVER_USER_KEY")
    api_token = os.getenv("PUSHOVER_API_TOKEN")

    if not user_key or not api_token:

        return {
            "success": False,
            "message": "Pushover credentials are not configured."
        }

    try:
        response = requests.post(
            PUSHOVER_API_URL,
            data={
                "token": api_token,
                "user": user_key,
                "title": title,
                "message": message,
            },
            timeout=10,
        )
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Failed to reach Pushover: {e}"
        }

    if response.ok:

        return {
            "success": True,
            "message": "Notification sent successfully."
        }

    return {
        "success": False,
        "message": f"Pushover error: {response.text}"
    }