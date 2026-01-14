"""
Script to put data from text files into DB, in table 'segments'
"""
import os
import json
import sqlite3

##################################################

base_path = './sutta-data'

db = 'sutta-pitaka.sqlite'

##################################################

print(f'Begin to work...')

raw_data = []

counter = 1

for filename in sorted(os.listdir(base_path)):
    if not filename.lower().endswith('.json'):
        continue

    file_path = os.path.join(base_path, filename)

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    file_id = os.path.splitext(filename)[0]
    
    file_id = file_id.split('_translation', 1)[0]
    
    for line_id, text in data.items():
         
        raw_data.append((file_id, line_id, text, counter))
        counter += 1

print(f'Read {len(raw_data)} strings from files')  # 245733

##################################################

line_ids = (row[1] for row in raw_data)   # генератор, не копирует данные
s = set()

for x in line_ids:
    if x in s:
        raise AssertionError(f'Duplicate segment_id: {x}')
    s.add(x)

##################################################

db_data = []

skipped = 0

prev_is_empty = False

for (file_id, segment_id, text, row_id) in raw_data:

    # book — до первой точки или до двоеточия, что раньше

    #an9.29:1.4
    #pli-tv-kd11:31.1.185
    
    s = segment_id
    book = s[:min(x if x != -1 else len(s) for x in (s.find('.'), s.find(':')))]

    ####
    
    # sutta — до двоеточия
    sutta = segment_id.split(':', 1)[0]
    
    content = text.strip()
    
    if content.isdigit(): # like empty strings
        content = ''
        
    if content.startswith('Numbered Discourses'):
        skipped += 1
        continue
    
    is_empty = (content == '')

    if is_empty and prev_empty:
        skipped += 1
        continue   # skip consecutive empty lines
    
    prev_empty = is_empty        
    
    db_data.append((row_id, segment_id, book, file_id, sutta, content))

print(f'Skipped {skipped} strings')

db_data.sort(key=lambda x: x[0]) #  sorted by row_id

db_data = [row[1:] for row in db_data] #  and delete row_id from data

##################################################

with sqlite3.connect(db) as conn:
    
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM segments')
    
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'segments' ")
    
    cursor.executemany('''
        INSERT INTO segments
        (segment_id, book, chapter, sutta, content)
        VALUES (?, ?, ?, ?, ?)
    ''', db_data)
    
    inserted = cursor.rowcount
    
    conn.commit()

print(f'Insert {inserted} rows into database')

assert ( len(raw_data) == skipped+inserted ), 'Something wrong...'

##################################################

print(f'Job finished')    
    