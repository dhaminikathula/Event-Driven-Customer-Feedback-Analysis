CREATE DATABASE IF NOT EXISTS feedback_db;
USE feedback_db;
CREATE TABLE IF NOT EXISTS feedback_analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    feedback_text TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    compound_score FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
