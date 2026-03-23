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

STRICT RULES:
- Answer ONLY questions related to Christ Nagar College
- Use ONLY the college information provided below — no outside knowledge
- If the question is not related to the college, respond exactly: "I can only answer questions about Christ Nagar College. Please ask something relevant."
- If the answer is not in the college data, respond exactly: "I don't have that information. Please contact the college office at 0471-XXXXXXX"
- If the user sends gibberish, nonsense, or inappropriate content, respond exactly: "I can only answer questions about Christ Nagar College. Please ask something relevant."
- Never engage with general knowledge questions
- Never engage with inappropriate content
- Keep answers concise and clear

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