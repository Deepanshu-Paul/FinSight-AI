import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


def call_llm(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        content = response.choices[0].message.content

        if not content:
            return None  # IMPORTANT

        return content.strip()

    except Exception as e:
        print("LLM ERROR:", e)
        return None  # IMPORTANT (not fallback text)


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
        return call_llm(prompt)

    except Exception as e:
        print("LLM Error:", e)

        # ✅ Strong fallback (keep this)
        if total == 0:
            return "No transaction data available."

        fraud_rate = (fraud / total) * 100 if total > 0 else 0

        if fraud_rate < 1:
            level = "low"
        elif fraud_rate < 5:
            level = "moderate"
        else:
            level = "high"

        return (
            f"Fraud rate is {fraud_rate:.2f}%, indicating a {level} level of fraudulent activity. "
            f"This may be due to unusual transaction patterns or anomalies that should be investigated."
        )