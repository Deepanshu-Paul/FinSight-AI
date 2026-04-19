import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise Exception("❌ GROQ_API_KEY not found")

client = Groq(api_key=GROQ_API_KEY)

print("🚀 Sending request to Groq...\n")

try:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # fast + free tier friendly
        messages=[
            {"role": "user", "content": "Explain fraud detection in simple terms."}
        ],
        temperature=0.3,
    )

    print("✅ SUCCESS\n")
    print("OUTPUT:\n")
    print(response.choices[0].message.content)

except Exception as e:
    print("❌ ERROR:", str(e))