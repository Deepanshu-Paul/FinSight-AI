import os
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

if not HF_API_KEY:
    raise Exception("❌ HF_API_KEY not found. Check your .env file")

# ✅ Correct endpoint
url = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

payload = {
    "inputs": "Fraud detection test query"
}

print("🚀 Sending request to Hugging Face...\n")

try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
        proxies={
            "http": "",
            "https": ""
        }
    )

    print("----- DEBUG INFO -----")
    print("Status Code:", response.status_code)
    print("Final URL Hit:", response.url)
    print("Headers:", response.headers)
    print("Raw Response (first 500 chars):\n", response.text[:500])

    # Try parsing JSON safely
    try:
        data = response.json()
        print("\n✅ JSON parsed successfully")

        # Handle embedding format
        if isinstance(data, list):
            if isinstance(data[0], list):
                print("Vector length:", len(data[0]))
            else:
                print("Vector length:", len(data))

    except Exception as e:
        print("\n❌ JSON parsing failed:", str(e))

except Exception as e:
    print("\n❌ Request failed:", str(e))