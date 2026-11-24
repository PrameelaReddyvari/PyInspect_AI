
from pathlib import Path
from dotenv import load_dotenv
from google import genai
import os

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: API key not found.")
else:
    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents="Explain Python functions in two simple sentences."
        )

        print("SUCCESS!")
        print(response.text)

    except Exception as error:
        print("GEMINI TEST FAILED:")
        print(repr(error))
