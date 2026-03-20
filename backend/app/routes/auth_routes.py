from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(login_data: LoginRequest):
    if login_data.username == "admin" and login_data.password == "1234":
        return {"token": "abc123"}
    
    raise HTTPException(status_code=401, detail="Invalid login")