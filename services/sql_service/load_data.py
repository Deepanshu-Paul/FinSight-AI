import csv
import os
import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv

# Load env variables
load_dotenv()

print("Connecting to DB...")

conn = psycopg2.connect(
    os.getenv("DATABASE_URL"),
    sslmode="require"   # important for Render
)

cur = conn.cursor()
print("Connected!")

# Resolve file path (works locally)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
file_path = os.path.join(BASE_DIR, "data", "raw", "fraud.csv")

print(f"Reading file from: {file_path}")

# Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    amount FLOAT,
    is_fraud INT
)
""")

# Clear existing data (optional)
cur.execute("TRUNCATE TABLE transactions;")
print("Table ready")

# Read CSV
data = []

with open(file_path, "r") as f:
    reader = csv.DictReader(f)

    for i, row in enumerate(reader):
        data.append((row["Amount"], row["Class"]))

        # progress log
        if i % 10000 == 0:
            print(f"Loaded {i} rows into memory")

print(f"Total rows loaded: {len(data)}")

# Batch insert (FAST)
print("Inserting into DB...")

execute_batch(
    cur,
    "INSERT INTO transactions (amount, is_fraud) VALUES (%s, %s)",
    data,
    page_size=1000
)

conn.commit()

print("✅ Data inserted successfully!")

cur.close()
conn.close()

print("🎉 Done!")