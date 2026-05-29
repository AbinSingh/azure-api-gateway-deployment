from fastapi import FastAPI
import socket

app = FastAPI()

@app.get("/users")
def get_users():
    return {
        "service": "user-service",
        "pod": socket.gethostname(),
        "users": ["Alice", "Bob"]
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }
