import sqlite3

#########################################################
#########################################################
#########################################################

MAX_TOKENS = 800

db = 'sutta-pitaka.sqlite'

#########################################################

with sqlite3.connect(db) as conn:
    
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM chunks ORDER BY id')
    chunks = cursor.fetchall()    

    cursor.execute('SELECT * FROM segments ORDER BY row_id')
    segments_by_id = {row["row_id"]: row for row in cursor.fetchall()}  

#########################################################
#########################################################
#########################################################

UPD_CHUNKS = []

BIG_CHUNKS_IDS = []

for chunk in chunks:
    
    updated_chunk = {}
    
    updated_chunk['id'] = chunk['id']
    
    ###########################################       
    
    start_row_id = chunk['start_row_id'] 
    
    assert start_row_id in segments_by_id
    
    start_seg_id = segments_by_id[start_row_id]['segment_id']
    
    if chunk["start_seg_id"] is not None:
           
           assert chunk["start_seg_id"] == start_seg_id
    
    updated_chunk['start_seg_id'] = start_seg_id
    
    ###########################################       

    end_row_id = chunk['end_row_id'] 
    
    assert end_row_id in segments_by_id
    
    end_seg_id = segments_by_id[end_row_id]['segment_id']
    
    if chunk["end_seg_id"] is not None:
        
        assert chunk["end_seg_id"] == end_seg_id
    
    updated_chunk['end_seg_id'] = end_seg_id
    
    ###########################################       

    lines = []
    
    for row_id in range(start_row_id, end_row_id + 1):

          text = segments_by_id[row_id]['content']

          lines.append(text)
    
    chunk_content = "\n".join(lines)
    
    updated_chunk['content'] = chunk_content
    
    updated_chunk['tokens'] = len(chunk_content)//4
    
    if updated_chunk['tokens'] > MAX_TOKENS:
              
              BIG_CHUNKS_IDS.append(chunk['id'])

    ###########################################      
    
    UPD_CHUNKS.append(updated_chunk)

#########################################################
#########################################################
#########################################################


#########################################################
#########################################################
#########################################################

print('Job finished')    
    
