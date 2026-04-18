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

from fastapi.responses import HTMLResponse

@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
    <html>
    <head>
        <title>FinSight AI</title>
    </head>
    <body style="font-family: Arial; padding: 40px;">
        <h1>FinSight AI Dashboard</h1>

        <h2>Fraud Summary</h2>
        <button onclick="getSummary()">Load Summary</button>
        <pre id="summary"></pre>

        <h2>Fraud Insight (AI)</h2>
        <button onclick="getInsight()">Generate Insight</button>
        <pre id="insight"></pre>

        <h2>Ask Custom Question (RAG)</h2>
        <input id="query" style="width:300px;" placeholder="Ask something..." />
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

@app.get("/ask")
def ask(q: str):
    from services.rag_service.retriever import retrieve
    from services.llm_service.llm import generate_explanation

    context = retrieve(q)

    prompt = f"""
    You are a financial fraud expert.

    Context:
    {''.join(context)}

    Question:
    {q}

    Answer clearly.
    """

    # reuse LLM logic (slight modification needed)
    from services.llm_service.llm import call_llm

    answer = call_llm(prompt)

    return {
        "question": q,
        "context": context,
        "answer": answer
    }