# christ_nagar_chatbot
A chatbot for Christ Nagar College

## Tech Stack
FastAPI + Groq (llama-3.3-70b-versatile)

## Setup
1. Create venv and activate it
2. Run: pip install -r requirements.txt
3. Create .env file for keeping the api key
4. Update college_data.txt with real college information
5. Run: uvicorn main:app --reload

## API
POST /chat
Request: { "message": "user's question" }
Response: { "response": "AI's answer" }
