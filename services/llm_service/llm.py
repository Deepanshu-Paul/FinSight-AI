from services.rag_service.retriever import retrieve
import requests

def generate_explanation(total, fraud):
    context = retrieve("fraud analysis explanation")

    prompt = f"""
    You are a financial fraud analyst.

    Context:
    {''.join(context)}

    Data:
    Total transactions: {total}
    Fraud transactions: {fraud}

    Provide a grounded explanation using the context.
    """

    response = requests.post(
        "http://host.docker.internal:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]