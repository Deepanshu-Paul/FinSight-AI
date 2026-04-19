import csv
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

# ✅ Create table automatically
cur.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    amount FLOAT,
    is_fraud INT
)
""")

# OPTIONAL: clear table to avoid duplicates
cur.execute("TRUNCATE TABLE transactions;")

# Load CSV
with open('/app/data/raw/fraud.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cur.execute(
            "INSERT INTO transactions (amount, is_fraud) VALUES (%s, %s)",
            (row['Amount'], row['Class'])
        )

conn.commit()
cur.close()
conn.close()

print("Data loaded successfully")