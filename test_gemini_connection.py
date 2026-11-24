
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

print("Starting Gemini connection test...", flush=True)

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: API key not found in .env")
    raise SystemExit

print("API key loaded successfully.", flush=True)
print("Connecting to Google Gemini...", flush=True)

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"

headers = {
    "Content-Type": "application/json",
    "x-goog-api-key": api_key
}

payload = {
    "contents": [
        {
            "parts": [
                {"text": "Explain Python variables in simple English."}
            ]
        }
    ]
}

try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=20
    )

    print("HTTP Status:", response.status_code, flush=True)

    if response.ok:
        data = response.json()
        print("\nGemini Explanation:")
        print(data["candidates"][0]["content"]["parts"][0]["text"])
    else:
        print("\nGoogle API Error:")
        print(response.text)

except requests.exceptions.Timeout:
    print("ERROR: Google API request timed out.")

except requests.exceptions.RequestException as error:
    print("Connection error:", str(error))
