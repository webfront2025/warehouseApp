# import os
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Vi definerer en router i stedet for en app
# router = APIRouter()

# class ChatRequest(BaseModel):
#     message: str

# @router.post("/ai/chat")
# async def chat_with_ai(request: ChatRequest):
#     # try:
#     #     response = client.chat.completions.create(
#     #         model="gpt-3.5-turbo",
#     #         messages=[
#     #             {"role": "system", "content": "You are a helpful assistant for StockFlow."},
#     #             {"role": "user", "content": request.message}
#     #         ]
#     #     )
#     #     return {"reply": response.choices.message.content}
#     return {"reply": f"Dette er et testsvar fra StockFlow AI.Du spurgte om: {request.message}"}
#     # except Exception as e:
#     #     raise HTTPException(status_code=500, detail=str(e))

#                   ----------------  22-04-2026 ----- install Ollama from Docker   ---------------

from fastapi import APIRouter
from pydantic import BaseModel
import requests
# from app.rag.search import search

from app.ai.sql_agent import ask_database, extract_product_name
from app.ai.tool_router import decide_tool
from app.ai.tools import get_low_stock_products, get_all_products

router = APIRouter()

# ✅ memory for last product
last_product = None

class ChatRequest(BaseModel):
    message: str

@router.post("/api/ai/chat")
async def chat_with_ai(request: ChatRequest):
    global last_product
    sql = None
    data = []

    try:
        user_msg = request.message.lower().strip()
        product = extract_product_name(user_msg)

        if product:
            last_product = product
        if not product and last_product:
            user_msg = f"{user_msg} {last_product}"

        # =========================
        # SPECIAL: COMPARE PRODUCTS
        # =========================
        if "compare" in user_msg:
            products_list = []
            for word in user_msg.split():
                _, result = ask_database(word)
                if result:
                    row = result[0]
                    products_list.append(f"{row[0]} ({row[1]} pcs)")
            if products_list:
                return {
                     "reply": "Comparison:\n• " + "\n• ".join(products_list)
}

        # =========================
        # SPECIAL: IS LOW STOCK?
        # =========================
            if "low stock" in user_msg and product and "show" not in user_msg:            sql, data = ask_database(product)
            if data:
                qty = data[0][1]
                if qty < 20:
                    return {"reply": f"Yes, {product} is low stock ({qty} left)."}
                else:
                    return {"reply": f"No, {product} has {qty} units."}

        # 1. TOOL DECISION
        tool = decide_tool(user_msg)

        # 2. EXECUTE TOOL
        if tool == "low_stock":
            data = get_low_stock_products()
        elif tool == "all_products":
            data = get_all_products()
        else:
            sql, data = ask_database(user_msg)

        # 3. EMPTY RESULT
        if not data:
            return {"reply": "Not in stock", "sql": sql, "data": []}

        # 4. SMART PICK BEST MATCH
        first = data[0]
        try:
            if last_product:
                for row in data:
                    if str(row[0]).lower() == last_product.lower():
                        first = row
                        break
        except:
            pass

        # 5. NORMALIZE DATA
        if len(first) == 2:
            name = first[0]

            if any(x in user_msg for x in ["price", "how much", "cost"]):
                price = first[1]
                qty = None
            else:
                qty = first[1]
                price = None

        elif len(first) == 3:
            name, qty, price = first[0], first[1], first[2]

        elif len(first) >= 5:
            name, price, qty = first[1], first[3], first[4]

        else:
            name, qty, price = str(first[0]), "?", None

        # 6. RESPONSE RULES
        if tool == "low_stock":
            lines = [f"{row[0]} ({row[1]} left)" for row in data]
            reply = "Low stock products:\n" + "\n".join(lines)
        elif tool == "all_products":
            lines = [f"{row[0]} - Qty:{row[1]}" for row in data]
            reply = "All products:\n" + "\n".join(lines)
        elif any(x in user_msg for x in ["price", "how much", "cost"]):
            reply = f"{name} costs {price if price else 'unknown'} kr."
        elif "how many" in user_msg or "quantity" in user_msg:
            reply = f"We have {qty} units of {name}."
        else:
            reply = f"Yes, we have {name} in stock. Quantity: {qty}"

        return {"reply": reply, "sql": sql, "data": data}

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}


        # 2. Create the context string 
        #context = "Here is the current warehouse stock:\n"
       ## for p in products:
            #context += f"Product: {p[1]}, Quantity: {p[2]}\n" # Adjusted indices based on typical DB rows
        #    context += f"- Product: {p[0]} ({p[1]}), Stock: {p[2]} units\n"
        # 3. Combine context with the user message 
        #full_prompt = f"{context}\n\nUser Question: {request.message}\nAssistant:"
        #system_instruction = "You are a warehouse assistant. Use this data to answer: "
        #full_prompt = f"{system_instruction}{context}\nUser: {request.message}\nAI Assistant:"
       # full_prompt = f"""
       # You are a StockFlow warehouse assistant.
       # RULES:
       # 1. Answer ONLY using the inventory data below.
       # 2. If a product is not mentioned in the inventory, say "Not in stock".
       # 3. Be very brief and professional.

       # INVENTORY:
       # {context}

       # USER QUESTION: 
       # {request.message}

       # ANSWER:
       # """

        # 4. Send everything to Ollama and get the response
        #response = requests.post(
          #  "http://localhost:11434/api/generate",
          #  json={
          #      "model": "llama3",
          #      "prompt": prompt,
          #      "stream": False
          #  }
       # )

       # result = response.json()
       # return {"reply": result.get("response", "No response"),
         #       "sql": sql,
         #       "data": db_result}

   # except Exception as e:
   #     return {"error": str(e)}



