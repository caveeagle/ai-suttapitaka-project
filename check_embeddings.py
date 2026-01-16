import sqlite3

#########################################################
#########################################################
#########################################################

DELETE_WRONG_EMBEDDINGS = 0 #  Delete or ignore

#########################################################
#########################################################
#########################################################

db = 'sutta-pitaka.sqlite'

with sqlite3.connect(db) as conn:
    
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM chunks ORDER BY id')
    chunks = {row['id']: row for row in cursor.fetchall()}      

    cursor.execute('SELECT * FROM embeddings ORDER BY chunk_id')
    embeddings = cursor.fetchall()  

#########################################################
#########################################################
#########################################################

WRONG_EMBEDDINGS = [] 

for emb in embeddings:
    
    chunk_id = emb['chunk_id']
    
    orig_hash = chunks[chunk_id]['chunk_hash']
    
    if( emb['chunk_hash'] != orig_hash ):
        
        WRONG_EMBEDDINGS.append(chunk_id)

if( len(WRONG_EMBEDDINGS)==0 ):
    
    print(f'ALL EMBEDDINGS ARE OK.')

else:
    
    print(f'Find {len(WRONG_EMBEDDINGS)} wrong embeddings.')

#########################################################
#########################################################
#########################################################

if DELETE_WRONG_EMBEDDINGS:
    
    if len(WRONG_EMBEDDINGS) != 0 :

        placeholders = ','.join('?' * len(WRONG_EMBEDDINGS))
        
        cursor.execute(
            f'DELETE FROM embeddings WHERE chunk_id IN ({placeholders})',
            WRONG_EMBEDDINGS
        )
        
        deleted = cursor.rowcount
        
        conn.commit()
        
        print(f'Delete {deleted} records')
    
#########################################################
#########################################################
#########################################################

print('Job finished')    
    
