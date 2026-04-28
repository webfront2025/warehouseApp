import requests

def decide_tool(user_msg):
    user_msg = user_msg.lower()

    # 1. Quick check for simple keywords (Fast)
    if "low stock" in user_msg:
        return "low_stock"
    if "all products" in user_msg:
        return "all_products"

    # 2. If no keywords, ask the AI to decide (Smart)
    prompt = f"""
    You are an AI assistant.
    Decide which tool to use.

    Available tools:
    1. low_stock
    2. all_products
    3. sql

    Return ONLY the tool name.

    User: {user_msg}
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=2
        )
        decision = response.json().get("response", "").strip().lower()
        
        # Make sure the AI returns a valid tool name
        if "low_stock" in decision: return "low_stock"
        if "all_products" in decision: return "all_products"
        return "sql"
        
    except Exception:
        return "sql" # Fallback to SQL if AI fails
