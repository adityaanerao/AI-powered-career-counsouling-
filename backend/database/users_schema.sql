-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    interests TEXT,
    skills TEXT,
    subjects TEXT,
    exam_details JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User History Table
CREATE TABLE IF NOT EXISTS user_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action_type VARCHAR(50) NOT NULL, -- e.g., 'CAREER_SEARCH', 'COLLEGE_CHECK'
    details JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Index for faster history retrieval
CREATE INDEX idx_history_user ON user_history(user_id);
