CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    title TEXT,
    created_by INTEGER,
    visible INTEGER DEFAULT 1,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    thread_id INTEGER,
    created_by INTEGER,
    visible INTEGER DEFAULT 1,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    pass TEXT,
    admin BOOLEAN DEFAULT FALSE,
    visible INTEGER DEFAULT 1,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE thanks (
    id SERIAL PRIMARY KEY,
    thread_id INTEGER,
    message_id INTEGER,
    created_by INTEGER,
    visible INTEGER DEFAULT 1
);
