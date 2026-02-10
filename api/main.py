# Entry point for REST API
# Accepts sentiment requests and publishes messages to Kafka
from fastapi import FastAPI
app = FastAPI()
@app.get("/health")
def health_check():
    return {"status": "ok"}
