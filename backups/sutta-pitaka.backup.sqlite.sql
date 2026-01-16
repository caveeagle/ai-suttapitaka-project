BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS chapters_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter TEXT NOT NULL,
    rows_count INTEGER NOT NULL,
    total_chars INTEGER NOT NULL,
    start_row_id INTEGER NOT NULL,
    start_segment_id TEXT NOT NULL,
    end_row_id INTEGER NOT NULL,
    end_segment_id TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "chunks" (
	"id"	INTEGER,
	"chapter"	TEXT NOT NULL,
	"content"	TEXT,
	"start_row_id"	INTEGER NOT NULL,
	"end_row_id"	INTEGER NOT NULL,
	"start_seg_id"	TEXT,
	"end_seg_id"	TEXT,
	"tokens"	INTEGER,
	"chunk_hash"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "embeddings" (
	"chunk_id"	INTEGER UNIQUE,
	"embedding"	BLOB,
	"chunk_hash"	TEXT,
	PRIMARY KEY("chunk_id")
);
CREATE TABLE IF NOT EXISTS segments (
    row_id INTEGER PRIMARY KEY AUTOINCREMENT,
    segment_id TEXT UNIQUE,
    book TEXT,
    chapter TEXT,
    sutta TEXT,
    content TEXT
);
CREATE INDEX idx_chunks_start_end
ON chunks (start_row_id, end_row_id);
CREATE INDEX idx_segments_chapter_row
ON segments (chapter, row_id);
COMMIT;
