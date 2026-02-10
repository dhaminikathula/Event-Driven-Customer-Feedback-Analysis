# Kafka consumer that processes messages asynchronously
import json
import time
from kafka import KafkaConsumer

def main():
    print("🚀 Worker starting...", flush=True)

    while True:
        try:
            print("⏳ Connecting to Kafka...", flush=True)

            consumer = KafkaConsumer(
                "sentiment_topic",
                bootstrap_servers="kafka:9092",
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset="earliest",
                group_id="feedback-worker-group",
            )

            print("✅ Connected to Kafka. Waiting for messages...", flush=True)

            for message in consumer:
                print("📩 Received message:", message.value, flush=True)

        except Exception as e:
            print("❌ Kafka not ready, retrying in 5 seconds...", e, flush=True)
            time.sleep(5)

if __name__ == "__main__":
    main()
