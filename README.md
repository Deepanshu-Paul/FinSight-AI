# FinSight AI — Intelligent Fraud Analysis & Financial Insight Assistant

---

## Overview

**FinSight AI** is a data-driven assistant designed to help understand financial transactions, detect unusual activity, and provide clear explanations using both data and regulatory knowledge.

It combines structured transaction data with unstructured documents (such as banking guidelines) to answer questions, explain fraud patterns, and surface insights in plain language.

---

## What It Does

FinSight AI acts like a smart analyst that:

- Looks at transaction data to identify unusual patterns  
- Explains why certain transactions may be suspicious  
- Answers questions about fraud trends and financial activity  
- Connects real data with regulatory guidelines for better context  

Instead of manually analyzing data and documents, users can simply ask questions and get clear, contextual answers.

---

## Key Features

- 📊 **Fraud Trend Analysis**  
  Understand how fraud activity changes over time  

- 🔍 **Anomaly Explanation**  
  Get human-readable explanations for suspicious transactions  

- 📄 **Document-Aware Insights (RAG)**  
  Answers are grounded using regulatory documents (e.g., RBI guidelines)  

- 🔗 **Multi-Source Intelligence**  
  Combines:
  - transaction data  
  - system logs  
  - external documents  

- ⚡ **Natural Language Querying**  
  Ask questions like:
  - “Why did fraud increase last week?”  
  - “Explain this suspicious transaction”  

---

## High-Level Architecture

User Query
    ↓
API (FastAPI)
    ↓
Query Router
    ↓
 ┌───────────────┬────────────────┬──────────────┐
 │ SQL Service   │ RAG Service    │ Log Retrieval│
 │ (Postgres)    │ (FAISS + LLM)  │              │
 └───────────────┴────────────────┴──────────────┘
                ↓
            Context Builder
                ↓
            LLM (Ollama)
                ↓
            Final Response

            
