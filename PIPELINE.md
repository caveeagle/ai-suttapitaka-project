# A way to reproduce the results

1. Clone repository `ai-suttapitaka-project`
2. Install python packages from `requirements.txt`
3. Unzip files from `./backups/sutta-data.zip` to `sutta-data` dir
4. Create sqlite DB `sutta-pitaka.sqlite` in the project dir
5. Create tables with file `./backups/sutta-pitaka.backup.sqlite.sql`
6.  Create `secret_config.py` with variable API_KEY = 'AI****' with yor API key for Gooogle AI
7. Run `make_db_from_text.py` - it fills the table `segments`
8. Run `make_table_chapters.sql` sql file, it fills the table `chapters_info`
9. Run script `make_chunks_borders.py` it makes chunks borders in the table `chunks`
10. Run script `make_chunks_content.py` - it fills chunk's content in the table `chunks`
11. Run script `make_embedding.py`as many times as needed - it fills `embeddings` table
12. Run `check_embeddings.py` 