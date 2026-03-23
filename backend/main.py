from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app=FastAPI()
client=Groq(api_key=os.getenv("GROQ_API_KEY"))


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str


def load_college_data():
    with open("college_data.txt", "r") as f:
        return f.read()

@app.post("/chat")
async def chat(request: ChatRequest):
    college_data = load_college_data()
    
    system_prompt = f"""You are a helpful assistant for Christ Nagar College, Trivandrum.
Answer questions only based on the information provided below.
If the answer is not found in the information, say "I don't have that information. Please contact the college office directly at 0471-XXXXXXX"
Do not use any outside knowledge. Only use what is provided below.

--- COLLEGE INFORMATION ---
{college_data}
"""
    
    response = client.chat.completions.create(
        model=os.getenv("MODEL_NAME"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.message}
        ]
    )
    
    return {"response": response.choices[0].message.content}