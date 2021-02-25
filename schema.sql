CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR (32) UNIQUE,
    pass TEXT,
    admin BOOLEAN DEFAULT FALSE,
    visible BOOLEAN DEFAULT TRUE,
    banned BOOLEAN DEFAULT FALSE,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE forums (
    id SERIAL PRIMARY KEY,
    name VARCHAR (120) UNIQUE,
    visible BOOLEAN DEFAULT TRUE
);

CREATE TABLE subforums (
    id SERIAL PRIMARY KEY,
    name VARCHAR (120),
    descri VARCHAR (240),
    forum_id INTEGER,
    visible BOOLEAN DEFAULT TRUE,
    UNIQUE (name, forum_id),
    FOREIGN KEY (forum_id) REFERENCES forums (id)
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    title VARCHAR (120) NOT NULL,
    subforum_id INTEGER,
    created_by INTEGER,
    visible BOOLEAN DEFAULT TRUE,
    locked BOOLEAN DEFAULT FALSE,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (title, subforum_id),
    FOREIGN KEY (subforum_id) REFERENCES subforums (id),
    FOREIGN KEY (created_by) REFERENCES users (id)
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    thread_id INTEGER,
    created_by INTEGER,
    sent_to INTEGER,
    visible BOOLEAN DEFAULT TRUE,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (thread_id) REFERENCES threads (id),
    FOREIGN KEY (created_by) REFERENCES users (id),
    FOREIGN KEY (sent_to) REFERENCES users (id)
);

CREATE TABLE thanks (
    id SERIAL PRIMARY KEY,
    thread_id INTEGER,
    message_id INTEGER,
    created_by INTEGER,
    visible BOOLEAN DEFAULT TRUE,
    UNIQUE (thread_id, created_by),
    UNIQUE (message_id, created_by),
    FOREIGN KEY (thread_id) REFERENCES threads (id),
    FOREIGN KEY (message_id) REFERENCES messages (id),
    FOREIGN KEY (created_by) REFERENCES users (id)
);





