from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from services.api_gateway.db import get_connection
from services.llm_service.llm import call_llm
from services.rag_service.retriever import retrieve

app = FastAPI()

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Frontend
# -----------------------------
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def home():
    return FileResponse("frontend/index.html")


# -----------------------------
# Health
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
# Fraud Insight (RAG + LLM)
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

    context = retrieve("fraud detection patterns")

    prompt = f"""
    You are a financial fraud analyst.

    Data:
    - Total transactions: {total}
    - Fraud transactions: {fraud}

    Context:
    {''.join(context)}

    Explain:
    - What this fraud rate indicates
    - Possible reasons
    - Any patterns
    """

    explanation = call_llm(prompt)

    return {
        "total": total,
        "fraud": fraud,
        "context_used": context,
        "insight": explanation
    }


# -----------------------------
# RAG Chat
# -----------------------------
@app.get("/ask")
def ask(q: str):
    context = retrieve(q)

    prompt = f"""
    You are a senior financial fraud analyst.

    Context:
    {''.join(context)}

    Question:
    {q}

    Rules:
    - Use bullet points
    - Be concise
    - Explain like advising a business team
    """

    answer = call_llm(prompt)

    return {
        "type": "text",
        "answer": answer
    }


# -----------------------------
# DB Chat (SQL + Insight + Chart)
# -----------------------------
@app.get("/ask-db")
def ask_db(q: str):
    try:
        # -----------------------------
        # STEP 1: Generate SQL
        # -----------------------------
        sql_prompt = f"""
        You are a PostgreSQL expert.

        Table:
        transactions(id, amount, is_fraud INTEGER)

        IMPORTANT:
        - is_fraud uses 1 = fraud, 0 = not fraud
        - NEVER use true/false

        Rules:
        - Only SELECT queries
        - No explanation
        - Return ONLY SQL

        Examples:

        Q: count fraud transactions  
        A: SELECT COUNT(*) FROM transactions WHERE is_fraud = 1;

        Q: total transactions  
        A: SELECT COUNT(*) FROM transactions;

        Q: fraud vs normal  
        A: SELECT is_fraud, COUNT(*) FROM transactions GROUP BY is_fraud;

        Now convert:

        {q}
        """

        sql_query = call_llm(sql_prompt)

        if not sql_query:
            return {"type": "error", "message": "LLM failed to generate SQL"}

        # -----------------------------
        # STEP 2: Clean SQL
        # -----------------------------
        sql_query = str(sql_query)
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        sql_query = sql_query.replace("true", "1").replace("false", "0")

        if not sql_query.lower().startswith("select"):
            return {
                "type": "error",
                "message": "Invalid SQL generated",
                "query": sql_query
            }

        print("SQL:", sql_query)

        # -----------------------------
        # STEP 3: Execute SQL
        # -----------------------------
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(sql_query)
        result = cur.fetchall()

        columns = [desc[0] for desc in cur.description]

        cur.close()
        conn.close()

        # -----------------------------
        # STEP 4: Generate explanation
        # -----------------------------
        data_preview = result[:10]

        explain_prompt = f"""
        You are a senior financial fraud analyst.

        User question:
        {q}

        Result:
        {data_preview}

        Structure:

        Summary:
        - What this shows

        Key Insights:
        - 2–3 insights

        Risk Interpretation:
        - What this means

        Recommendation:
        - What to do
        """

        explanation = call_llm(explain_prompt)

        return {
            "type": "table_with_explanation",
            "columns": columns,
            "rows": result if result else [["No data found"]],
            "explanation": explanation or "No explanation available"
        }

    except Exception as e:
        print("ERROR:", e)
        return {
            "type": "error",
            "message": str(e)
        }