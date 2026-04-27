import requests


def decide_tool(user_message: str):
    prompt = f"""
You are an AI assistant.

Decide which tool to use.

Available tools:
1. get_low_stock_products
2. get_all_products
3. none

Return ONLY tool name.

User:
{user_message}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    decision = response.json().get("response", "").strip().lower()

    return decision