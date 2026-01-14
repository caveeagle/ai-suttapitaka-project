import sqlite3

#########################################################
#########################################################
#########################################################

db = 'sutta-pitaka.sqlite'

MAX_TOKENS_IN_CHAPTER = 800

#########################################################
#########################################################
#########################################################

SMALL_CHAPTERS = []

BIG_CHAPTERS = []

with sqlite3.connect(db) as conn:
    
    cursor = conn.cursor()
    
    SQL_QUERY = f'''
            SELECT chapter
            FROM segments
            GROUP BY chapter
            HAVING SUM(LENGTH(content)) < {MAX_TOKENS_IN_CHAPTER*4};
    '''
    
    cursor.execute(SQL_QUERY)

    SMALL_CHAPTERS = [row[0] for row in cursor.fetchall()]
    
    print('Small chapters:',len(SMALL_CHAPTERS))    

    SQL_QUERY = f'''
            SELECT chapter
            FROM segments
            GROUP BY chapter
            HAVING SUM(LENGTH(content)) >= {MAX_TOKENS_IN_CHAPTER*4};
    '''
    
    cursor.execute(SQL_QUERY)

    BIG_CHAPTERS = [row[0] for row in cursor.fetchall()]
    
    print('Big chapters:',len(BIG_CHAPTERS))    
    
    SQL_QUERY = 'SELECT COUNT(DISTINCT chapter) AS total_chapters FROM segments'
    
    cursor.execute(SQL_QUERY)
    
    total_chapters = cursor.fetchone()[0]
    
    print(f'total={total_chapters}')
    
    assert total_chapters == len(BIG_CHAPTERS) + len(SMALL_CHAPTERS)
    
#########################################################
#########################################################
#########################################################




#########################################################
#########################################################
#########################################################


print('Job finished')    
    
