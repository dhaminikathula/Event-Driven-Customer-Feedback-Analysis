# Kafka consumer that processes messages asynchronously
import json
import time
import nltk
import mysql.connector
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")

def get_db_connection():
    while True:
        try:
            return mysql.connector.connect(
                host="mysql",
                user="root",
                password="root",
                database="feedback_db"
            )
        except Exception as e:
            print("MySQL not ready, retrying in 5 seconds...", flush=True)
            time.sleep(5)

def main():
    print("Worker starting (resilient mode)...", flush=True)

    sia = SentimentIntensityAnalyzer()
    db = get_db_connection()
    cursor = db.cursor()

    consumer = None

    while True:
        try:
            if consumer is None:
                print("Connecting to Kafka (worker)...", flush=True)
                consumer = KafkaConsumer(
                    "sentiment_topic",
                    bootstrap_servers="kafka:9092",
                    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                    auto_offset_reset="earliest",
                    group_id="feedback-worker-group",
                )
                print("✅ Kafka connected (worker). Waiting for messages...", flush=True)

            for message in consumer:
                feedback = message.value["text"]
                scores = sia.polarity_scores(feedback)

                sentiment = (
                    "Positive" if scores["compound"] >= 0.05 else
                    "Negative" if scores["compound"] <= -0.05 else
                    "Neutral"
                )

                cursor.execute(
                    """
                    INSERT INTO feedback_analysis
                    (feedback_text, sentiment, compound_score)
                    VALUES (%s, %s, %s)
                    """,
                    (feedback, sentiment, scores["compound"])
                )
                db.commit()

                print("Stored feedback:", sentiment, flush=True)

        except NoBrokersAvailable:
            print("Kafka not ready (worker). Retrying in 5 seconds...", flush=True)
            consumer = None
            time.sleep(5)

        except Exception as e:
            print("❌ Worker error:", e, flush=True)
            time.sleep(5)

if __name__ == "__main__":
    main()
