import asyncio
import json
import random
import uuid
from aiokafka import AIOKafkaProducer
import datetime

TOPIC = "orders"
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"

REGION = "worldwide"

event_count = 0
clients = []
producer = None
run_flag = False


def change_region() -> str:
    """Toggle the region between Poland and Worldwide."""
    global REGION
    REGION = "poland" if REGION == "worldwide" else "worldwide"
    return REGION

def generate_order(client_id: int) -> dict:
    """Generate a random order with client ID and realistic values."""

    # Price ranges based on products
    price_ranges = {
        "laptop": (500, 2000),
        "keyboard": (50, 200),
        "mouse": (30, 200),
        "monitor": (60, 500),
        "headphones": (30, 400),
        "phone": (100, 1500)
    }

    product = random.choice(list(price_ranges.keys()))
    low, high = price_ranges[product]
    price = round(random.uniform(low, high), 2)

    user_id = random.randint(1, 1000)
    
    if REGION == "poland":
        region = "PL"
    else:
        # Region based on user_id mod
        mod = user_id % 10
        if 0 <= mod < 4:
            region = "US"
        elif mod < 6:
            region = "UK"
        elif mod < 8:
            region = "DE"
        elif mod < 9:
            region = "FR"
        else:
            region = "PL"

    return{
        "order_id": str(uuid.uuid4()),
        "user_id": user_id,
        "product": product,
        "price": price,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "region": region,
        "client_id": client_id
    }


async def client_loop(client_id: int):
    """Client event loop that generates and sends orders to Kafka."""
    global event_count
    while run_flag:
        order = generate_order(client_id)
        await producer.send_and_wait(TOPIC, json.dumps(order).encode("utf-8"))
        print(f"Client {client_id}, sent: {order}")
        event_count += 1
        await asyncio.sleep(random.uniform(0.1, 1.0)) # different intervals


async def start_clients(num_clients: int):
    """Start the specified number of client loops and the Kafka producer."""
    global clients, producer, run_flag
    if run_flag:
        return # Already running
    
    run_flag = True
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()

    clients = [asyncio.create_task(client_loop(i)) for i in range(num_clients)]


async def stop_clients():
    """Stop all clients and shut down the Kafka producer."""
    global clients, producer, run_flag
    run_flag = False

    await asyncio.gather(*clients, return_exceptions=True)
    clients = []

    await producer.stop()


def get_stats() -> dict:
    """Return basic statistics about event generation."""
    return{
        "clients_active": len(clients),
        "events_sent": event_count,
        "running": run_flag
    }