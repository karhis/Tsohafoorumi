CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    title TEXT,
    created_by INTEGER,
    date TIMESTAMP
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    thread_id INTEGER,
    created_by INTEGER,
    date TIMESTAMP
);
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    pass TEXT,
    admin, BOOLEAN,
    date TIMESTAMP
);
CREATE TABLE thanks (
    id SERIAL PRIMARY KEY,
    thread_id INTEGER,
    message_id INTEGER,
    created_by INTEGER
);
