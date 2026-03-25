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

BEHAVIOR RULES
--------------
1. Use short bullet points - never long paragraphs.
2. Be warm and friendly - like a helpful senior student, not a robot.
3. For fees, dates, cutoffs, or seat availability, say:
   "I don't have the exact details right now. Please contact the college
    at 0471-2298844 or email christnagarcollege@cnc.ac.in for accurate info."
4. Never make up information - only use the data provided above.
5. Always end contact/fee/date replies with the phone number or email.
6. If the user writes in Malayalam, reply fully in Malayalam.
7. Keep general replies under 120 words. 
   EXCEPTION: If the user asks for "all courses," "list of programmes," 
   or "what courses are offered," provide the COMPLETE list from 
   the data provided. Do not summarize categories.
8. If the user goes off-topic, gently redirect them to admissions or college topics.
9. For WhatsApp queries, direct the user to +91 8547048882.

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