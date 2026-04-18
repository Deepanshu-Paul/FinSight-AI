from fastapi import FastAPI
from services.api_gateway.db import get_connection
from services.llm_service.llm import generate_explanation

app = FastAPI()


@app.get("/")
def root():
    return {"message": "FinSight AI is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/fraud-summary")
def fraud_summary():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*), COALESCE(SUM(is_fraud), 0)
            FROM transactions
        """)

        total, fraud = cur.fetchone()

        cur.close()
        conn.close()

        return {
            "total_transactions": total,
            "fraud_transactions": fraud
        }

    except Exception as e:
        print(f"DB Error: {e}")
        return {
            "total_transactions": 0,
            "fraud_transactions": 0,
            "message": "Database not available"
        }


@app.get("/fraud-insight")
def fraud_insight():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*), COALESCE(SUM(is_fraud), 0)
            FROM transactions
        """)

        total, fraud = cur.fetchone()

        cur.close()
        conn.close()

    except Exception as e:
        print(f"DB Error: {e}")
        total, fraud = 0, 0

    # Always attempt LLM (but it may fallback)
    explanation = generate_explanation(total, fraud)

    return {
        "total": total,
        "fraud": fraud,
        "insight": explanation
    }