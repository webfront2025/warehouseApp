def decide_route(user_message: str):
    message = user_message.lower()

    # simple smart rules
    if "do you have" in message or "stock" in message or "how many" in message:
        return "sql"

    if "what is" in message or "explain" in message:
        return "rag"

    return "rag"  # default