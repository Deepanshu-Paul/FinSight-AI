import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")


def call_llm(prompt):
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-base",
            headers={
                "Authorization": f"Bearer {HF_API_KEY}"
            },
            json={
                "inputs": prompt
            },
            timeout=30
        )

        print("HF STATUS:", response.status_code)

        # 🔁 Handle cold start (very common)
        if response.status_code == 503:
            print("⏳ Model loading... retrying in 5 sec")
            import time
            time.sleep(5)

            response = requests.post(
                "https://api-inference.huggingface.co/models/google/flan-t5-base",
                headers={
                    "Authorization": f"Bearer {HF_API_KEY}"
                },
                json={
                    "inputs": prompt
                },
                timeout=30
            )

        # ❌ Still failing
        if response.status_code != 200:
            print("HF ERROR:", response.status_code, response.text)
            return "LLM unavailable (fallback response)"

        data = response.json()
        print("HF RESPONSE:", data)

        # ✅ Normal HF format
        if isinstance(data, list) and len(data) > 0:
            return data[0].get("generated_text", "No response")

        # ⚠️ Sometimes HF returns dict
        if isinstance(data, dict):
            return data.get("generated_text", str(data))

        return str(data)

    except Exception as e:
        print("LLM Exception:", e)
        return "LLM unavailable (fallback response)"


def generate_explanation(total, fraud):
    """
    Generate explanation using LLM.
    Falls back safely if LLM is unavailable.
    """

    prompt = f"""
    You are a financial fraud analyst.

    Total transactions: {total}
    Fraud transactions: {fraud}

    Calculate fraud percentage and explain what this indicates.
    Keep it simple and professional.
    """

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-base",
            headers={
                "Authorization": f"Bearer {HF_API_KEY}"
            },
            json={
                "inputs": prompt
            },
            timeout=30
        )

        if response.status_code != 200:
            print("HF ERROR:", response.text)
            raise Exception("HF failed")

        data = response.json()

        if isinstance(data, list):
            return data[0].get("generated_text", "No response")

        return str(data)

    except Exception as e:
        print(f"LLM Error: {e}")

        # ✅ Fallback logic (kept from your version)
        if total == 0:
            return "No transaction data available."

        fraud_rate = (fraud / total) * 100 if total > 0 else 0

        return (
            f"Fraud rate is approximately {fraud_rate:.2f}%. "
            f"This is a basic system-generated insight (LLM unavailable)."
        )