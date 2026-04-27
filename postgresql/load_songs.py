from pathlib import Path
import importlib
import os

import numpy as np

pd = importlib.import_module("pandas")
StandardScaler = importlib.import_module("sklearn.preprocessing").StandardScaler

# ── Config ──────────────────────────────────────────────────────────────
DB_URL = os.getenv(
    "POSTGRES_URL",
    "host=localhost port=5432 dbname=music_recommender user=postgres password=postgres",
)
EMBEDDING_DIM = 100
BATCH_SIZE = 1000


def build_embedding_frame(songs):
    numeric_columns = ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]
    categorical_columns = ["genre", "mood"]

    numeric_frame = songs[numeric_columns].fillna(0.0).astype(float)
    numeric_scaled = StandardScaler().fit_transform(numeric_frame)
    numeric_frame = pd.DataFrame(numeric_scaled, columns=numeric_columns, index=songs.index)

    categorical_frame = pd.get_dummies(songs[categorical_columns].fillna(""), prefix=categorical_columns)
    embedding_frame = pd.concat([numeric_frame, categorical_frame], axis=1)

    if embedding_frame.shape[1] < EMBEDDING_DIM:
        padding = pd.DataFrame(
            0.0,
            index=embedding_frame.index,
            columns=[f"pad_{i}" for i in range(EMBEDDING_DIM - embedding_frame.shape[1])],
        )
        embedding_frame = pd.concat([embedding_frame, padding], axis=1)

    return embedding_frame.iloc[:, :EMBEDDING_DIM]


data_path = Path(__file__).resolve().parents[1] / "data" / "songs.csv"
print(f"Loading songs from {data_path}...")
songs = pd.read_csv(data_path)
print(f"  {len(songs)} songs found")

print("Building embeddings...")
embedding_frame = build_embedding_frame(songs)

print(f"Loading {len(songs)} rows into PostgreSQL...")
psycopg2 = importlib.import_module("psycopg2")
execute_values = importlib.import_module("psycopg2.extras").execute_values

rows = []
for row_index, song in songs.iterrows():
    embedding = embedding_frame.loc[row_index].astype(float).tolist()
    rows.append(
        (
            int(song["id"]),
            str(song.get("title", "") or ""),
            str(song.get("artist", "") or ""),
            "",
            str(song.get("genre", "") or ""),
            str(song.get("mood", "") or ""),
            float(song.get("energy", 0.0) or 0.0),
            float(song.get("tempo_bpm", 0.0) or 0.0),
            float(song.get("valence", 0.0) or 0.0),
            float(song.get("danceability", 0.0) or 0.0),
            float(song.get("acousticness", 0.0) or 0.0),
            0.0,
            embedding,
        )
    )

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

# Keep schema in sync with src.main query even when DB volume was created earlier.
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS songs (
      id           INT PRIMARY KEY,
      title        TEXT,
      artist       TEXT,
      album        TEXT,
      genre        TEXT,
      mood         TEXT,
      energy       FLOAT,
      tempo_bpm    FLOAT,
      valence      FLOAT,
      danceability FLOAT,
      acousticness FLOAT,
      duration     FLOAT,
      embedding    vector(100)
    );
    """
)
for column, column_type in [
    ("mood", "TEXT"),
    ("energy", "FLOAT"),
    ("tempo_bpm", "FLOAT"),
    ("valence", "FLOAT"),
    ("danceability", "FLOAT"),
    ("acousticness", "FLOAT"),
]:
    cur.execute(f"ALTER TABLE songs ADD COLUMN IF NOT EXISTS {column} {column_type};")

cur.execute("TRUNCATE TABLE songs;")

for i in range(0, len(rows), BATCH_SIZE):
    batch = rows[i:i + BATCH_SIZE]
    execute_values(
        cur,
        """
        INSERT INTO songs (
            id, title, artist, album, genre, mood, energy, tempo_bpm,
            valence, danceability, acousticness, duration, embedding
        )
        VALUES %s
        ON CONFLICT (id) DO UPDATE SET
            title = EXCLUDED.title,
            artist = EXCLUDED.artist,
            album = EXCLUDED.album,
            genre = EXCLUDED.genre,
            mood = EXCLUDED.mood,
            energy = EXCLUDED.energy,
            tempo_bpm = EXCLUDED.tempo_bpm,
            valence = EXCLUDED.valence,
            danceability = EXCLUDED.danceability,
            acousticness = EXCLUDED.acousticness,
            duration = EXCLUDED.duration,
            embedding = EXCLUDED.embedding
        """,
        batch,
        template="(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::vector)",
    )
    conn.commit()

cur.close()
conn.close()
print("Done.")

after_load_sql = Path(__file__).with_name("run-after-data-loads.sql")
if after_load_sql.exists():
    print("Running post-load SQL...")
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(after_load_sql.read_text(encoding="utf-8"))
    conn.commit()
    cur.close()
    conn.close()
    print("Post-load SQL complete.")
