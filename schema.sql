CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    title TEXT,
    subforum_id INTEGER,
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
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_to INTEGER
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
CREATE TABLE forums (
    id SERIAL PRIMARY KEY,
    name TEXT,
    visible INTEGER DEFAULT 1
);
CREATE TABLE subforums (
    id SERIAL PRIMARY KEY,
    name TEXT,
    descri TEXT,
    forum_id INTEGER,
    visible INTEGER DEFAULT 1
)
