# Entry point for REST API
# Accepts sentiment requests and publishes messages to Kafka
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from producer import send_message
import uuid

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze")
def analyze_text(request: TextRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    message = {
        "id": str(uuid.uuid4()),
        "text": request.text
    }

    send_message(message)

    return {
        "status": "queued",
        "message_id": message["id"]
    }
