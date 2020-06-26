CREATE TABLE reviews
(
  reviewno SERIAL PRIMARY KEY,
  uid INTEGER,
  FOREIGN KEY(uid) REFERENCES users(userid),
  bid INTEGER,
  FOREIGN KEY(bid) REFERENCES books,
  rating SMALLINT,
  comments VARCHAR
);
