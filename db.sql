CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password) VALUES ('user1', 'password1');
INSERT INTO users (username, password) VALUES ('user2', 'password2');

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    client_id INTEGER, 
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    start_day DATE,
    end_day DATE,
    total_data_count INTEGER DEFAULT 0,
    annotated_data_count INTEGER DEFAULT 0,
    max_annotations_per_user INTEGER,
    threshold DECIMAL(5, 4)
);

INSERT INTO tasks (client_id, title, description, status, start_day, end_day, total_data_count, annotated_data_count, max_annotations_per_user, threshold) 
VALUES (1, '機械翻訳の評価', '英日翻訳の正確さを3段階で評価してください', '進行中', '2025-08-01', '2025-08-07', 100, 0, 20, 0.5);