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
# from app.ai.tool_router import decide_tool
# from app.ai.tools import get_low_stock_products, get_all_products

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
            
      #  if user did NOT mention product → reuse last one
        if not product and last_product:
            user_msg = f"{user_msg} {last_product}"

        print("FINAL USER MSG:", user_msg)
        print("LAST PRODUCT:", last_product)

        # -----------------------------
        # STEP 3: query database
        # -----------------------------
        sql, db_result = ask_database(user_msg)

        print("SQL:", sql)
        print("DB RESULT:", db_result)

        # -----------------------------
        # STEP 4: handle empty result
        # -----------------------------
        if not db_result or db_result == []:
            return {
                "reply": "Not in stock",
                "sql": sql,
                "data": db_result
            }

        # 5. Build AI response (Ollama)
#         prompt = f"""
# You are a warehouse assistant.

# Database result:
# {db_result}

# User question:
# {user_msg}

# Rules:
# - Answer ONLY using the database result above
# - If price exists → show price
# - If quantity exists → show quantity
# - Be very short and clear

# Answer:
# """
#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             json={
#                 "model": "llama3",
#                 "prompt": prompt,
#                 "stream": False
#             },
#             timeout=10  # Prevent hanging if Ollama is slow
#         )
        
#         result = response.json()
#         return {
#             "reply": result.get("response", "No response from AI"),
#             "sql": sql,
#             "data": db_result
#         }

# Simple smart reply without Ollama

        first = db_result[0]
        for row in db_result:
            if row[0].lower() == last_product.lower():
                 first = row
            break

        if "price" in user_msg:
            reply = f"{first[0]} costs {first[1]} kr."
        elif "how many" in user_msg or "quantity" in user_msg:
            reply = f"We have {first[1]} units of {first[0]}."
        else:
            reply = f"Yes, we have {first[0]} in stock. Quantity: {first[1]}"

        return {
            "reply": reply,
            "sql": sql,
            "data": db_result
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



