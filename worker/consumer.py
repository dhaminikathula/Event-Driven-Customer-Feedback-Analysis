# Kafka consumer that processes messages asynchronously
import json
import time
import nltk
import mysql.connector
from kafka import KafkaConsumer
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")

def get_db_connection():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="feedback_db"
    )

def main():
    print("Worker started with sentiment + MySQL", flush=True)

    sia = SentimentIntensityAnalyzer()
    db = get_db_connection()
    cursor = db.cursor()

    while True:
        try:
            consumer = KafkaConsumer(
                "sentiment_topic",
                bootstrap_servers="kafka:9092",
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset="earliest",
                group_id="feedback-worker-group",
            )

            print("✅ Kafka connected. Waiting for messages...", flush=True)

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

                print("📩 Saved to DB:", feedback, sentiment, flush=True)

        except Exception as e:
            print("❌ Error:", e, flush=True)
            time.sleep(5)

if __name__ == "__main__":
    main()
