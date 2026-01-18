import time
import numpy as np
import sqlite3
from google import genai

import secret_config
from model_indexing import build_index, search

from google.genai.errors import ClientError

#########################################################
#########################################################

DEBUG = 1

TOP_K = 5

#MODEL = 'gemini-2.0-flash-lite'
MODEL = 'gemini-2.5-pro'


QUESTION = (
    'According to the Buddha, which sensory experiences '
    'most strongly occupy a man’s mind?'
)

#########################################################
#########################################################

PROMPT_TEMPLATE = """
You answer questions using ONLY the provided sources.

Each source is marked as [CHAPTER <id>].

Rules:
- Use ONLY information that is explicitly present in the sources.
- If the answer is NOT present in the sources, output exactly:
  The answer is not found in the provided sources.
- Do NOT use outside knowledge.
- Do NOT invent sources.
- Do NOT invent CHUNK IDs.
- Follow the output format exactly.

Question:
{question}

Sources:
{sources}

Output format (must be exact):

Answer:
<answer OR the no-answer sentence>

Sources:
<comma-separated CHAPTER IDs, or empty if no answer>
"""

#########################################################
#########################################################

print(f'Begin to work...')

API_KEY = secret_config.API_KEY

if not API_KEY or not API_KEY.strip():
    raise ValueError('API_KEY is empty or not set')

client = genai.Client(api_key=API_KEY)

index, chunk_ids = build_index()

resp = client.models.embed_content(
    model='models/text-embedding-004',
    contents=[QUESTION],
)

time.sleep(2)

print(f'Question embedded!')

query_vec = np.array(resp.embeddings[0].values, dtype=np.float32)

top_chunk_ids, scores = search(index, chunk_ids, query_vec, k=TOP_K)

if(DEBUG):
    print(f'Find top chunks ids: {top_chunk_ids}')

#########################################################
#########################################################

db = 'sutta-pitaka.sqlite'

context_lines = []

placeholders = ','.join('?' for _ in top_chunk_ids)

query = f'''
SELECT *
FROM chunks
WHERE id IN ({placeholders})
ORDER BY id
'''

with sqlite3.connect(db) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(query, top_chunk_ids)
    rows = cursor.fetchall()
    
content_blocks = []

for row in rows:
    content_blocks.append(
        f"[CHAPTER {row['chapter']}]\n{row['content']}"
    )

SOURCES = '\n\n'.join(content_blocks)

print(f'Make content blocks, ready for request:')

#########################################################
#########################################################

PROMPT = PROMPT_TEMPLATE.format(
    question=QUESTION,
    sources=SOURCES
)

try:
    response = client.models.generate_content(
        model=MODEL,
        contents=[PROMPT],
    )

except ClientError as e:
    msg = str(e)

    if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
        print(f'ERROR 429 - LIMITS EXCEEDED!')
        # просто выходим, ничего не выводим
        pass
    else:
        raise
    
print(f'Request finished.\n\n')
    
#########################################################
#########################################################

### OUTPUT:

print('\nQUESTION:')
print(QUESTION)
print('\nANSWER:')
print(response.text)

print(f'\n\nJob finished')

#########################################################
#########################################################
