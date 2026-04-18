import requests


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
            "http://host.docker.internal:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=5
        )

        return response.json().get("response", "No response from LLM")

    except Exception as e:
        print(f"LLM Error: {e}")

        # ✅ Fallback logic (important for deployment)
        if total == 0:
            return "No transaction data available."

        fraud_rate = (fraud / total) * 100 if total > 0 else 0

        return (
            f"Fraud rate is approximately {fraud_rate:.2f}%. "
            f"This is a basic system-generated insight (LLM unavailable)."
        )