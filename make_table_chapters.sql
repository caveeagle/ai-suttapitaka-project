
##################################################

CREATE INDEX IF NOT EXISTS idx_segments_chapter_row
ON segments (chapter, row_id);

##################################################

SELECT
    segments_outer.chapter,
    COUNT(*) AS rows_count,
    SUM(LENGTH(segments_outer.content)) AS total_chars,

    MIN(segments_outer.row_id) AS start_row_id,
    (
        SELECT segments.segment_id
        FROM segments
        WHERE segments.chapter = segments_outer.chapter
        ORDER BY segments.row_id ASC
        LIMIT 1
    ) AS start_segment_id,

    MAX(segments_outer.row_id) AS end_row_id,
    (
        SELECT segments.segment_id
        FROM segments
        WHERE segments.chapter = segments_outer.chapter
        ORDER BY segments.row_id DESC
        LIMIT 1
    ) AS end_segment_id

FROM segments AS segments_outer
GROUP BY segments_outer.chapter;

##################################################

INSERT INTO chapters_info (
    chapter,
    rows_count,
    total_chars,
    start_row_id,
    start_segment_id,
    end_row_id,
    end_segment_id
)
SELECT
    segments_outer.chapter,
    COUNT(*) AS rows_count,
    SUM(LENGTH(segments_outer.content)) AS total_chars,

    MIN(segments_outer.row_id) AS start_row_id,
    (
        SELECT segments.segment_id
        FROM segments
        WHERE segments.chapter = segments_outer.chapter
        ORDER BY segments.row_id ASC
        LIMIT 1
    ) AS start_segment_id,

    MAX(segments_outer.row_id) AS end_row_id,
    (
        SELECT segments.segment_id
        FROM segments
        WHERE segments.chapter = segments_outer.chapter
        ORDER BY segments.row_id DESC
        LIMIT 1
    ) AS end_segment_id
FROM segments AS segments_outer
GROUP BY segments_outer.chapter;

##################################################

