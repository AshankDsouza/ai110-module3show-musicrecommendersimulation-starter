CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS songs (
	id          INT PRIMARY KEY,
	title       TEXT,
	artist      TEXT,
	album       TEXT,
	genre       TEXT,
	duration    FLOAT,
	embedding   vector(100)
);
