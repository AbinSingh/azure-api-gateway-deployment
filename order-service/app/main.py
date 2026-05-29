from fastapi import FastAPI
import socket

app = FastAPI()

@app.get("/orders")
def get_orders():
    return {
        "service": "order-service",
        "pod": socket.gethostname(),
        "orders": [101, 102, 103]
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


