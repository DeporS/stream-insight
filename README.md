# stream-insight

## Order Generator

Located in `app/generator.py`. It simulates real-time order traffic by generating events asynchronously and sending them to a Kafka topic (`orders`)
- Multiple async clients simulate users placing random orders simultaneously
- Each order includes `product`, `price`, `user_id`, `region`, `timestamp`, and `client_id`
- Data is sent to Kafka using `aiokafka`

## Control via FastAPI

A FastAPI app lets you control the generator at runtime.

* Endpoints:
- POST | `/start` - Start generating events
- POST | `/stop` - Stop running clients
- GET | `/stats` - Get number of active clients and events sent

=====

## How to Run

1. Create Venv

python3 -m venv venv
source venv/bin/activate

2. Install dependencies

pip install requirements.txt

3. Run Kafka

In `#2` terminal `docker-compose up`

4. Start FastAPI server:

In `#1` terminal `uvicorn app.main:app --reload`

5. Open docs at `http://localhost:8000/docs` or use `curl`:

curl -X POST "http://localhost:8000/start?clients=20"
