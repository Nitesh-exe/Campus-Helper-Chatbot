from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ChatRequest(BaseModel):
    message: str
@app.post("/chat")
async def chat(request: ChatRequest):
    OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="API key not set in environment variable OPENAI_API_KEY")
        
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo", 
        "messages": [
            {"role": "system", "content": "You are a helpful campus assistant AI."},
            {"role": "user", "content": request.message}
        ]
    }
    response = requests.post(OPENAI_API_URL, json=payload, headers=headers)
    res_json = response.json()
    
    print("OpenAI API response:", res_json)

    #for hndling errors
    if response.status_code != 200:
        error_msg = res_json.get('error', {}).get('message', 'Unknown error from OpenAI API')
        raise HTTPException(status_code=500, detail=error_msg)
    if 'choices' not in res_json or len(res_json['choices']) == 0:
        raise HTTPException(status_code=500, detail="No response from AI model")

    #extract reply
    reply = res_json['choices'][0]['message']['content']
    return {"reply": reply}
