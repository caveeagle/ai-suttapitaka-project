import sqlite3
import math

#########################################################
#########################################################
#########################################################

db = 'sutta-pitaka.sqlite'

MAX_TOKENS_IN_CHAPTER = 800

OPTIMAL_TOKENS = 6
00

#########################################################
#########################################################
#########################################################

with sqlite3.connect(db) as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM chapters_info ORDER BY id')
    chapters_info = cursor.fetchall()    

#########################################################

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
        
        chunk['chapter'] = chapter
        chunk['start_row_id'] = start_row_id
        chunk['end_row_id'] = end_row_id
        chunk['start_seg_id'] = start_segment_id
        chunk['end_seg_id'] = start_segment_id
        
        chunks.add(chunk)
    
    else: # BIG chapter    

        num_of_splits = ( (total_chars/4) // OPTIMAL_TOKENS ) + 1

        str_per_split = math.ceil( (end_row_id - start_row_id + 1) / num_of_splits )
        
        for N in range( num_of_splits ):
            
            chunk['





#########################################################
#########################################################
#########################################################


print('Job finished')    
    
