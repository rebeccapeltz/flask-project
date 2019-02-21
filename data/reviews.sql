CREATE TABLE reviews (
 id SERIAL PRIMARY KEY,
 book_id INTEGER REFERENCES books (id),
 user_id INTEGER REFERENCES users (id),
 rating INTEGER,
 CHECK (rating > 0),
 CHECK (rating < 6)
);