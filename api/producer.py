# Kafka producer logic for publishing messages
import json
import os
import time
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sentiment_topic")

_producer = None

def get_producer():
    global _producer
    while _producer is None:
        try:
            _producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            print("✅ Kafka producer connected", flush=True)
        except NoBrokersAvailable:
            print("⏳ Kafka not ready (API). Retrying in 5 seconds...", flush=True)
            time.sleep(5)
    return _producer

def send_message(message: dict):
    producer = get_producer()
    producer.send(KAFKA_TOPIC, message)
    producer.flush()
