-- Delete existing tables.
DROP TABLE IF EXISTS peeps;
DROP SEQUENCE IF EXISTS peeps_id_seq;

DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS users_id_seq;

-- Recreate tables.
CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255)
);

CREATE SEQUENCE IF NOT EXISTS peeps_id_seq;
CREATE TABLE peeps (
    id SERIAL PRIMARY KEY,
    content VARCHAR(255),
    timestamp TIMESTAMP, -- YYYY-MM-DD hh:mm:ss
    user_id INT,
    constraint fk_user foreign key(user_id)
      references users(id)
      on delete cascade
);

-- Insert test records.
INSERT INTO users (username, email, password) VALUES ('JMcK4529', 'test@mail.co.uk', '8ca187c92a6a3892735ca9fdcc5af91f4f423ee8cda550158192cfe4219246ad');

INSERT INTO peeps (content, timestamp, user_id) VALUES ('Welcome to Chitter!', '2023-12-07 11:13:15', 1);