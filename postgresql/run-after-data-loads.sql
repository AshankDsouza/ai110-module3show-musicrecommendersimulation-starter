-- Run after data is loaded
CREATE INDEX IF NOT EXISTS songs_embedding_hnsw_idx
ON songs
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Verify
SELECT pg_size_pretty(pg_relation_size('songs_embedding_hnsw_idx'));