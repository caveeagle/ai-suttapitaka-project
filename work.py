import sqlite3
import math

#########################################################
#########################################################
#########################################################

db = 'sutta-pitaka.sqlite'

MAX_TOKENS_IN_CHAPTER = 800

OPTIMAL_TOKENS = 400  # 1 token = 4 chars

OVERLAP_TOKENS = 70  # ~10-20% of chunk

OVERLAP_STRINGS = OVERLAP_TOKENS // 17.5

#########################################################
#########################################################
#########################################################

with sqlite3.connect(db) as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM chapters_info ORDER BY id')
    chapters_info = cursor.fetchall()    

#########################################################
#########################################################
#########################################################

###   Make chunks structure with chunk's bounds (without text)

chunks = []

for (
    _,
    chapter,
    rows_count,
    total_chars,
    start_row_id,
    start_segment_id,
    end_row_id,
    end_segment_id,
) in chapters_info:

    if( total_chars//4 < MAX_TOKENS_IN_CHAPTER ): #  small chapter - one chunk
        
        chunk = {}
        
        chunk['chapter'] = chapter
        chunk['start_row_id'] = start_row_id
        chunk['end_row_id'] = end_row_id
        chunk['start_seg_id'] = start_segment_id
        chunk['end_seg_id'] = start_segment_id
        
        chunks.append(chunk)
    
    else: # BIG chapter    

        num_of_splits = ( (total_chars//4) // OPTIMAL_TOKENS ) + 1

        str_per_split = math.ceil( (end_row_id - start_row_id + 1) / num_of_splits )
        
        for N in range( num_of_splits ):
            
            chunk_start_shift = ( N * str_per_split) - OVERLAP_STRINGS
            
            if chunk_start_shift < 0:
                chunk_start_shift = 0
            
            chunk_end_shift = ( (N+1) * str_per_split) - 1
            
            chunk_end_shift += OVERLAP_STRINGS
            
            if( chunk_end_shift > (end_row_id-start_row_id) ):
                
                chunk_end_shift = end_row_id-start_row_id
            
            chunk = {}
            
            chunk['start_row_id'] = start_row_id + chunk_start_shift
            
            chunk['end_row_id'] = start_row_id + chunk_end_shift
            
            chunk['start_seg_id'] = None
            
            chunk['end_seg_id'] = None
            
            chunk['chapter'] = chapter
            
            chunks.append(chunk)

print(f'Make {len(chunks)} chunks')

#########################################################
#########################################################
#########################################################

###   Add chunks (without text) into DB 

with sqlite3.connect(db) as conn:
    cursor = conn.cursor()

    cursor.execute("DELETE FROM chunks")

    SQL = '''
    INSERT INTO chunks (
        chapter,
        start_row_id,
        end_row_id,
        start_seg_id,
        end_seg_id
    )
    VALUES (
        :chapter,
        :start_row_id,
        :end_row_id,
        :start_seg_id,
        :end_seg_id
    )
    '''

    cursor.executemany(SQL, chunks)
    inserted = cursor.rowcount
    conn.commit()

print(f'Inserted {inserted} rows into db')

#########################################################
#########################################################
#########################################################

'''

SELECT COUNT(*) AS bad_order
FROM chunks
WHERE start_row_id > end_row_id;


'''

#bad_order != 0 !!!!!



#########################################################
#########################################################
#########################################################

print('Job finished')    
    
