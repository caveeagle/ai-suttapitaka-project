import sqlite3
import time
import numpy as np
from google import genai

import secret_config

#########################################################
#########################################################
#########################################################

BATCH_SIZE = 16  # or 32

db = 'sutta-pitaka.sqlite'

#########################################################
#########################################################
#########################################################

print(f'Begin to work...')

with sqlite3.connect(db) as conn:
    
    cursor = conn.cursor()

    cursor.execute(f'''
    SELECT id, content, chunk_hash
    FROM chunks
    WHERE id NOT IN (
        SELECT chunk_id FROM embeddings
    )
    ORDER BY id
    LIMIT {BATCH_SIZE*100}
    ''')
    
    rows = cursor.fetchall()

print(f'\nSELECT {len(rows)} CHUNKS\n')
    
############################################

API_KEY = secret_config.API_KEY

if not API_KEY or not API_KEY.strip():
    raise ValueError('API_KEY is empty or not set')

client = genai.Client(api_key=API_KEY)

with sqlite3.connect(db) as conn:
    
    cursor = conn.cursor()
    
    for i in range(0, len(rows), BATCH_SIZE):
        
        batch = rows[i:i + BATCH_SIZE]
    
        texts = [row[1] for row in batch]
        
        try:
            
            response = client.models.embed_content(
                model="models/text-embedding-004",
                contents=texts   # list[str]
            )
            
            time.sleep(1.0)  # Wait before new request !
            
        except Exception as e:
            msg = str(e).lower()
        
            # 429 — rate limit
            if "429" in msg or "resource_exhausted" in msg or "rate limit" in msg:
                raise RuntimeError("Gemini API: rate limit (429)") from e
        
            # 400 — bad request (пустой текст, слишком длинный и т.п.)
            if "400" in msg or "invalid" in msg or "bad request" in msg:
                raise ValueError("Gemini API: bad request (400)") from e
        
            # 401 / 403 — auth / permissions
            if "401" in msg or "403" in msg or "unauthorized" in msg or "permission" in msg:
                raise PermissionError("Gemini API: auth/permission error") from e
        
            # 500 / 503 — server side
            if "500" in msg or "503" in msg or "internal" in msg or "unavailable" in msg:
                raise RuntimeError("Gemini API: server error (5xx)") from e
        
            # всё остальное
            raise RuntimeError("Gemini API: unexpected error") from e
        
        print(f'Recieved Embedding: (from {i} to {i + BATCH_SIZE} in {len(rows)})')
        
        ############################################################    
            
        for (chunk_id, _, chunk_hash), emb in zip(batch, response.embeddings):
            vec = np.array(emb.values, dtype=np.float32)       
            
            cursor.execute(
                '''
                INSERT INTO embeddings (chunk_id, chunk_hash, embedding)
                VALUES (?, ?, ?)
                ''',
                (chunk_id, chunk_hash, vec.tobytes())
            )
            
            conn.commit()
        
        print(f'Add batch into DB\n')
        
        

        
#########################################################
#########################################################
#########################################################

print('Job finished')    
    
