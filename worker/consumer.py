# Kafka consumer that processes messages asynchronously
import json
import time
import nltk
from kafka import KafkaConsumer
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER lexicon (only once)
nltk.download("vader_lexicon")

def main():
    print("🚀 Worker started with sentiment analysis", flush=True)

    sia = SentimentIntensityAnalyzer()

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
                feedback = message.value["text"]

                scores = sia.polarity_scores(feedback)

                sentiment = (
                    "Positive" if scores["compound"] >= 0.05 else
                    "Negative" if scores["compound"] <= -0.05 else
                    "Neutral"
                )

                print("📩 Feedback:", feedback, flush=True)
                print("📊 Sentiment:", sentiment, scores, flush=True)

        except Exception as e:
            print("❌ Error. Retrying in 5 seconds:", e, flush=True)
            time.sleep(5)

if __name__ == "__main__":
    main()
