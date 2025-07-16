from fastapi import FastAPI, HTTPException
import asyncio
from app.generator import start_clients, stop_clients, get_stats

app = FastAPI()

@app.post("/start")
async def start(num_clients: int = 10):
    await start_clients(num_clients)
    return {"status": "started", "clients": num_clients}

@app.post("/stop")
async def stop():
    await stop_clients()
    return {"status": "stopped"}

@app.get("/stats")
async def stats():
    return get_stats()