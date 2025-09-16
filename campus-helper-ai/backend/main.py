from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Allow frontend to access backend API (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] if you want stricter
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model to validate incoming JSON
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    # OpenAI API URL and key (replace with your actual key)
    OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="API key not set in environment variable OPENAI_API_KEY")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",  # Using free tier compatible model
        "messages": [
            {"role": "system", "content": "You are a helpful campus assistant AI."},
            {"role": "user", "content": request.message}
        ]
    }

    # Call OpenAI API
    response = requests.post(OPENAI_API_URL, json=payload, headers=headers)
    res_json = response.json()

    # Debugging: print response
    print("OpenAI API response:", res_json)

    # Handle errors or missing keys
    if response.status_code != 200:
        error_msg = res_json.get('error', {}).get('message', 'Unknown error from OpenAI API')
        raise HTTPException(status_code=500, detail=error_msg)

    if 'choices' not in res_json or len(res_json['choices']) == 0:
        raise HTTPException(status_code=500, detail="No response from AI model")

    # Extract the AI reply
    reply = res_json['choices'][0]['message']['content']

    return {"reply": reply}
