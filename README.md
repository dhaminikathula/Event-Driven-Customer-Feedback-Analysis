# Event-Driven-Customer-Feedback-Analysis

 Overview:-

This project demonstrates an event-driven architecture for processing customer feedback using Kafka, performing sentiment analysis with NLTK, and storing results in MySQL, all orchestrated with Docker Compose.

🏗️ Architecture

Flow:

1. Client sends feedback to FastAPI endpoint

2. API publishes event to Kafka topic

3. Worker consumes events asynchronously

4. Sentiment analysis using NLTK VADER

5. Results stored in MySQL :-
    Client → API → Kafka → Worker → MySQL

🧰 Tech Stack :-
     => Python
     => FastAPI
     => Apache Kafka
     => NLTK (VADER)
     => MySQL
     => Docker & Docker Compose

⚙️ Setup Instructions
     -> Prerequisites
     -> Docker
     -> Docker Compose

Run the project :-
    => docker compose up --build

🔌 API Usage :-
    Endpoint
    POST http://localhost:8000/analyze


Sample Request :-
{
  "text": "The service was excellent and fast"
}


Response :-
{
  "status": "queued",
  "message_id": "uuid"
}

🗄️ Database Verification :-
    => docker compose exec mysql mysql -uroot -proot feedback_db
    => SELECT * FROM feedback_analysis;

📊 Sample Output :-
feedback_text	sentiment	compound_score
Great service	Positive	0.85

🧪 Features :-

--> Asynchronous event processing
--> Fault-tolerant Kafka consumer
-->NLP-based sentiment classification
--> Persistent storage
--> Fully dockerized setup

👨‍💻 Author

Dhamini Sri Raja Jahnavi Kathula