DROP TABLE IF EXISTS
  reservations,
  test_details,
  annotation_details,
  test_data,
  annotation_data,
  question_details,
  questions,
  tasks,
  users
CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    password VARCHAR NOT NULL
);

INSERT INTO users (name, password) VALUES ('user1', 'password1');
INSERT INTO users (name, password) VALUES ('user2', 'password2');
INSERT INTO users (name, password) VALUES ('user3', 'password3');

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR NOT NULL,
    description TEXT,
    private BOOLEAN NOT NULL,
    start_day DATE,
    end_day DATE,
    total_data_count INTEGER DEFAULT 0,
    annotated_data_count INTEGER DEFAULT 0,
    total_test_data_count INTEGER DEFAULT 0,
    max_annotations_per_user INTEGER,
    test BOOLEAN NOT NULL,
    threshold DECIMAL(5, 4)
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id),
    title VARCHAR NOT NULL
);

CREATE TABLE question_details (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES questions(id),
    description TEXT NOT NULL,
    scale VARCHAR
);

CREATE TABLE test_data (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id),
    data TEXT NOT NULL
);

CREATE TABLE test_details (
    id SERIAL PRIMARY KEY,
    test_id INTEGER NOT NULL REFERENCES test_data(id),
    question_detail_id INTEGER REFERENCES question_details(id),
    user_id INTEGER NOT NULL REFERENCES users(id)
);

CREATE TABLE annotation_data (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id),
    data TEXT NOT NULL
);

CREATE TABLE annotation_details (
    id SERIAL PRIMARY KEY,
    annotation_id INTEGER NOT NULL REFERENCES annotation_data(id),
    question_detail_id INTEGER REFERENCES question_details(id),
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id),
    annotation_data_id INTEGER NOT NULL REFERENCES annotation_data(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    UNIQUE (annotation_data_id),
    UNIQUE (user_id)
);

