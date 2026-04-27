CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS songs (
	id          INT PRIMARY KEY,
	title       TEXT,
	artist      TEXT,
	album       TEXT,
	genre       TEXT,
	mood        TEXT,
	energy      FLOAT,
	tempo_bpm   FLOAT,
	valence     FLOAT,
	danceability FLOAT,
	acousticness FLOAT,
	duration    FLOAT,
	embedding   vector(100)
);
