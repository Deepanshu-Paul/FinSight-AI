# test_groq.py

import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": "Return ONLY SQL: count fraud transactions"}
        ]
    }
)

print(response.status_code)
print(response.text)