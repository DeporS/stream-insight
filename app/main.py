from fastapi import FastAPI, HTTPException
import asyncio
from generator import start_clients, stop_clients, get_stats, change_region

app = FastAPI()

@app.post("/start")
async def start(num_clients: int = 10):
    """Start generating events with given number of clients."""
    await start_clients(num_clients)
    return {"status": "started", "clients": num_clients}

@app.post("/stop")
async def stop():
    """Stop all running clients."""
    await stop_clients()
    return {"status": "stopped"}

@app.post("/change_reg")
async def change_reg():
    """Toggle region between 'worldwide' and 'poland'."""
    region = change_region()
    return {"status": f"Region changed to {region}"}

@app.get("/stats")
async def stats():
    """Return stats about current generation state."""
    return get_stats()
