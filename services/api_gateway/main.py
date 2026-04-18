from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from services.api_gateway.db import get_connection
from services.llm_service.llm import generate_explanation, call_llm
from services.rag_service.retriever import retrieve

app = FastAPI()


# -----------------------------
# Root UI (Dashboard)
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>FinSight AI</title>
        <style>
            body { font-family: Arial; padding: 40px; background: #111; color: #eee; }
            button { padding: 10px; margin: 10px 0; cursor: pointer; }
            input { padding: 8px; width: 300px; }
            pre { background: #222; padding: 10px; border-radius: 5px; }
            h1 { color: #00ffcc; }
        </style>
    </head>
    <body>
        <h1>🚀 FinSight AI Dashboard</h1>

        <h2>📊 Fraud Summary</h2>
        <button onclick="getSummary()">Load Summary</button>
        <pre id="summary"></pre>

        <h2>🤖 Fraud Insight</h2>
        <button onclick="getInsight()">Generate Insight</button>
        <pre id="insight"></pre>

        <h2>🧠 Ask (RAG)</h2>
        <input id="query" placeholder="Ask about fraud..." />
        <button onclick="ask()">Ask</button>
        <pre id="answer"></pre>

        <script>
            async function getSummary() {
                const res = await fetch('/fraud-summary');
                const data = await res.json();
                document.getElementById('summary').innerText = JSON.stringify(data, null, 2);
            }

            async function getInsight() {
                const res = await fetch('/fraud-insight');
                const data = await res.json();
                document.getElementById('insight').innerText = data.insight;
            }

            async function ask() {
                const query = document.getElementById('query').value;
                const res = await fetch('/ask?q=' + encodeURIComponent(query));
                const data = await res.json();
                document.getElementById('answer').innerText = data.answer;
            }
        </script>
    </body>
    </html>
    """


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------
# Fraud Summary
# -----------------------------
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


# -----------------------------
# Fraud Insight (LLM)
# -----------------------------
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

    explanation = generate_explanation(total, fraud)

    return {
        "total": total,
        "fraud": fraud,
        "insight": explanation
    }


# -----------------------------
# RAG Query Endpoint
# -----------------------------
@app.get("/ask")
def ask(q: str):
    context = retrieve(q)

    prompt = f"""
    You are a financial fraud expert.

    Context:
    {''.join(context)}

    Question:
    {q}

    Provide a clear and concise answer.
    """

    answer = call_llm(prompt)

    return {
        "question": q,
        "context": context,
        "answer": answer
    }