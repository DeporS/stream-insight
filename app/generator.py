import asyncio
import json
import random
import uuid
from aiokafka import AIOKafkaProducer
import datetime

TOPIC = "orders"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"


def generate_order(client_id):
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


async def client(producer, client_id):
    while True:
        order = generate_order(client_id)
        await producer.send_and_wait(TOPIC, json.dumps(order).encode("utf-8"))
        print(f"Client {client_id}, sent: {order}")
        await asyncio.sleep(random.uniform(0.1, 1.0)) # different intervals


async def send_orders(num_clients=50):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    
    try:
        # Create and run tasks for all the clients
        tasks = [asyncio.create_task(client(producer, i)) for i in range(num_clients)]
        await asyncio.gather(*tasks) # Wait for all the tasks to finish

    finally:
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(send_orders(num_clients=10))