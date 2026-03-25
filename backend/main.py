from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# --- CACHING OPTIMIZATION: LOAD DATA ONCE AT STARTUP ---
def load_college_data():
    try:
        with open("college_data.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "College data not found."

COLLEGE_DATA = load_college_data()

# Define the SYSTEM_PROMPT globally so it is a static "Prefix" for Groq's cache
SYSTEM_PROMPT = f"""You are a helpful assistant for Christ Nagar College, Trivandrum.

BEHAVIOR RULES
--------------
1. Use short bullet points - never long paragraphs.
2. Be warm and friendly - like a helpful senior student, not a robot.
3. For fees, dates, cutoffs, or seat availability, say:
   "I don't have the exact details right now. Please contact the college
    at 0471-2298844 or email christnagarcollege@cnc.ac.in for accurate info."
4. Never make up information - only use the data provided below.
5. Always end contact/fee/date replies with the phone number or email.
6. If the user writes in Malayalam, reply fully in Malayalam.
7. Keep general replies under 120 words. 
   EXCEPTION: If the user asks for "all courses," "list of programmes," 
   or "what courses are offered," provide the COMPLETE list from 
   the data provided. Do not summarize categories.
8. If the user asks any question not in 'COLLEGE DATA', or asks about general knowledge, academic subjects, or off-topic 
   matters, you must strictly reply: 'I don't have that information. Please contact the college at 0471-2298844 for accurate details.'
9. For WhatsApp queries, direct the user to +91 8547048882.

--- COLLEGE INFORMATION ---
{COLLEGE_DATA}
"""

@app.post("/chat")
async def chat(request: ChatRequest):
    # Groq automatically caches the first message (system) if it stays identical.
    response = client.chat.completions.create(
        model=os.getenv("MODEL_NAME"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT}, # Static Prefix
            {"role": "user", "content": request.message}    # Dynamic User Message
        ],
        temperature=0 # CRITICAL: Ensures consistent output and strict data adherence
    )
    
    return {"response": response.choices[0].message.content}