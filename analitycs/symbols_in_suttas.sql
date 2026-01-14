SELECT
    chapter,
    SUM(LENGTH(content)) AS total_chars
FROM segments
GROUP BY chapter
ORDER BY total_chars DESC

#########################

SELECT COUNT(*) AS chapters_over
FROM (
    SELECT chapter
    FROM segments
    GROUP BY chapter
    HAVING SUM(LENGTH(content)) > 3200
);


## N = 884

#########################

SELECT chapter
FROM segments
GROUP BY chapter
HAVING SUM(LENGTH(content)) < 3200;
 
#########################

AVG. STRING in CHARS:

SELECT
    AVG(LENGTH(s.content)) AS avg_row_length
FROM segments s
JOIN (
    SELECT
        chapter
    FROM segments
    GROUP BY chapter
    HAVING SUM(LENGTH(content)) > 3200
) big_chapters
ON s.chapter = big_chapters.chapter;

### N = 70

#######################################

# Text by chapters

SELECT
    chapter,
    GROUP_CONCAT(content, '\n') AS chapter_text
FROM (
    SELECT
        chapter,
        content
    FROM segments
    ORDER BY chapter, row_id
)
GROUP BY chapter;


#######################################

