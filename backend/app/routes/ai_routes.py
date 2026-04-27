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
    # Initialize variables to avoid "undefined" errors
    data = []
    sql = None
    
    try:
        # 1. Get user message
        user_msg = request.message.lower().strip()

        # 2. Extract and manage product memory
        product = extract_product_name(user_msg)
        if product:
            last_product = product
        if not product and last_product:
            user_msg = f"{user_msg} {last_product}"

        print(f"FINAL USER MSG: {user_msg}")

        # 3. Decide and execute tool
        tool = decide_tool(user_msg)
        print(f"TOOL DECISION: {tool}")

        if "low_stock" in tool:
            data = get_low_stock_products()
        elif "all_products" in tool:
            data = get_all_products()
        else:
            # Fallback to SQL agent
            sql, data = ask_database(user_msg)

        print(f"DATA FOUND: {data}")

        # 4. Handle empty result
        if not data:
            return {
                "reply": "I'm sorry, I couldn't find that in the stock.",
                "sql": sql,
                "data": []
            }

        # 5. Build AI response (Ollama)
        prompt = f"""
You are a warehouse assistant.

Database result:
{data}

User question:
{user_msg}

Rules:
- Answer ONLY using the database result above
- If price exists → show price
- If quantity exists → show quantity
- Be very short and clear

Answer:
"""
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=120  # Prevent hanging if Ollama is slow
        )
        
        result = response.json()
        return {
            "reply": result.get("response", "No response from AI"),
            "sql": sql,
            "data": data
        }

    except Exception as e:
        print(f"ERROR: {str(e)}")
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



