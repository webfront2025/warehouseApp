import sqlite3
import requests
import os
import re
from app.database.database import DB_PATH

#  Correct database path

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# DB_PATH = os.path.join(BASE_DIR, "database.db")

print("USING DB:", DB_PATH)

def extract_product_name(question: str):
    words = question.lower().split()

    ignore = [
        "how", "many", "price", "what", "is",
        "do", "you", "have", "much", "the"
    ]

    keywords = [w for w in words if w not in ignore]

    if keywords:
        return keywords[-1]  # last meaningful word

    return None
#  1. Clean SQL from LLM output
def clean_sql(response_text):
    text = response_text.strip()
    match = re.search(r"```sql\n(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()

    if "SELECT" in response_text.lower():
        response_text = "SELECT " + response_text.split("SELECT",1)[1].split(";")[0] + ";"

    return response_text


#  2. Block dangerous SQL
def is_safe_sql(sql):
    forbidden = ["DELETE", "DROP", "UPDATE", "INSERT"]
    for word in forbidden:
        if word in sql.upper():
            return False
    if "SELECT" not in sql.upper():
        return False

    if "products" not in sql.lower():
        return False
    return True


#  3. Fix Danish letters ####      Normalize text
def normalize_text(text):
    text = text.lower().strip()

    # normalize Danish characters
    text = text.replace("ø", "æ")
    text = text.replace("ö", "ø")
    text = text.replace("oe", "ø")
    
    return text


# 4. Generate SQL using Ollama

def generate_sql(product_name: str, question: str):

    if not product_name:
        return None

    prompt = f"""
You are an SQL expert.

ONLY return SQL.
NO explanation.

Rules:
- ONLY SELECT
- Table: products(id, name, category, price, quantity)
- Use LIKE for product search

Question:
{question}

SQL:
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=10
        )

        ai_sql = response.json().get("response", "")
        clean = clean_sql(ai_sql)

        if is_safe_sql(clean):
            return clean

    except Exception as e:
        print("Ollama Error, fallback:", e)

    # ✅ fallback (VERY IMPORTANT)
    if "price" in question:
        return f"""
        SELECT name, price 
        FROM products 
         WHERE LOWER(name) LIKE '%' || LOWER('{product_name}') || '%';
        """

    elif "how many" in question or "quantity" in question:
        return f"""
        SELECT name, quantity 
        FROM products 
         WHERE LOWER(name) LIKE '%' || LOWER('{product_name}') || '%';
        """

    else:
        return f"""
        SELECT name, quantity 
        FROM products 
         WHERE LOWER(name) LIKE '%' || LOWER('{product_name}') || '%';
        """
        
#  MAIN FUNCTION
def ask_database(question: str):

    question = normalize_text(question)

    #  Ask Ollama to generate SQL
     #  extract product FIRST
    product_name = extract_product_name(question)

    if  product_name:
         product_name = normalize_text(product_name)
         
    if not product_name:
        return None, []

    sql = generate_sql(product_name, question)
    
    if not sql:
        return None, []

    print("PRODUCT:", product_name)
    print("SQL:", sql)
    
    if "how many" in question.lower():
        extra_rule = "- Return SUM(quantity)"
    else:
        extra_rule = "- Return name and quantity"

    if not is_safe_sql(sql):
        return None, []

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(sql)
        rows = cursor.fetchall()

        conn.close()

        return sql, rows

    except Exception as e:
        return sql, str(e)
