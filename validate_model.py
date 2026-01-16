import numpy as np
import sqlite3
from google import genai

import secret_config
from model_indexing import build_index, search

#########################################################
#########################################################

TOP_K = 5

MODEL = "gemini-2.0-flash-lite"

QUESTION = (
    "According to the Buddha, which sensory experiences "
    "most strongly occupy a man’s mind?"
)

#########################################################
#########################################################

API_KEY = secret_config.API_KEY

if not API_KEY or not API_KEY.strip():
    raise ValueError('API_KEY is empty or not set')

client = genai.Client(api_key=API_KEY)

index, chunk_ids = build_index()

resp = client.models.embed_content(
    model="models/text-embedding-004",
    contents=[QUESTION],
)

query_vec = np.array(resp.embeddings[0].values, dtype=np.float32)

top_chunk_ids, scores = search(index, chunk_ids, query_vec, k=TOP_K)

#########################################################
#########################################################

db = 'sutta-pitaka.sqlite'

context_lines = []

placeholders = ",".join("?" for _ in top_chunk_ids)

query = f"""
SELECT *
FROM chunks
WHERE id IN ({placeholders})
ORDER BY id
"""

with sqlite3.connect(db) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(query, top_chunk_ids)
    rows = cursor.fetchall()
    
contents = [row["content"] for row in rows]
   
context = "\n".join(contents)

#########################################################
#########################################################

PROMPT = f'''
Answer the question using only the provided sources.

Question:
{QUESTION}

Sources:
{context}

Answer concisely and cite the relevant sources.
'''


#########################################################
#########################################################

response = client.models.generate_content(
    model=MODEL,
    contents=[PROMPT],
)

#########################################################
#########################################################

# --- 6. Вывод ---
print("\nQUESTION:")
print(QUESTION)
print("\nANSWER:")
print(response.text)
print("\nSOURCES (chunk_id):")
print(list(top_chunk_ids))

print(f'Job finished')

#########################################################
#########################################################
