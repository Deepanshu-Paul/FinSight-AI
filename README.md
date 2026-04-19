# FinSight AI 🚀

FinSight AI is an end-to-end AI-powered financial analytics system that combines:
- 📊 Data dashboards
- 🧠 Retrieval-Augmented Generation (RAG)
- 🗄️ Natural language to SQL querying
- 🤖 LLM-based insights and explanations

---

## 🔥 Features

### 1. 📊 Interactive Dashboard
- Total transactions
- Fraud transactions
- Fraud rate
- Visual charts (donut, line, bar)

### 2. 🤖 AI Assistant
Ask questions like:
- "What are fraud patterns?"
- "Explain fraud rate"

Powered by:
- RAG (Qdrant)
- LLM (Groq - LLaMA 3)

---

### 3. 🗄️ Natural Language → SQL
Ask:
- "Count fraud transactions"
- "Show fraud vs normal"

System:
- Converts query → SQL
- Executes on PostgreSQL
- Returns results

---

### 4. 🧠 Analyst-Level Insights
Each query returns:
- Summary
- Key insights
- Risk interpretation
- Recommendations

---

### 5. 📈 Auto Chart Generation
If query includes grouping:
- Automatically renders charts
- No manual configuration

---

## 🏗️ Architecture

```
Frontend (HTML + JS)
        ↓
FastAPI Backend
        ↓
-------------------------
| RAG Service (Qdrant) |
| SQL DB (Postgres)   |
| LLM (Groq API)      |
-------------------------
```

---

## ⚙️ Tech Stack

- FastAPI (Backend)
- PostgreSQL (Database)
- Qdrant (Vector DB)
- Groq (LLM - LLaMA 3)
- Chart.js (Frontend charts)
- Vanilla JS + HTML (UI)

---

## 🚀 Getting Started

### 1. Clone Repo
```bash
git clone <your-repo-url>
cd FinSight-AI
```

### 2. Setup Environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate (Windows)
pip install -r requirements.txt
```

### 3. Configure `.env`
```
DATABASE_URL=your_postgres_url
GROQ_API_KEY=your_groq_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key
```

### 4. Run Backend
```bash
uvicorn main:app --reload
```

### 5. Open App
```
http://127.0.0.1:8000
```

---

## 🧪 Example Queries

### RAG
- What are fraud patterns?
- How does fraud detection work?

### DB Queries
- Count fraud transactions
- Show fraud vs normal
- Average transaction amount

---

## 🧠 Key Concepts

- **RAG**: Uses vector search to retrieve context
- **NL → SQL**: Converts natural language into SQL queries
- **LLM Insights**: Generates business-level explanations
- **Hybrid AI System**: Combines data + knowledge

---

## ⚠️ Notes

- Only SELECT queries are allowed (safe execution)
- LLM output is validated before execution
- Fallbacks prevent crashes

---

## 📌 Future Improvements

- Chat memory (multi-turn conversations)
- Streaming responses
- Advanced chart types (line, pie)
- Role-based access
- Deployment (Render / Railway)

---

## 💡 Why This Project?

This project demonstrates:
- Real-world AI system design
- Integration of LLM + databases
- Production-safe patterns
- Full-stack AI application

---

## 👨‍💻 Author

Deepanshu Paul

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
