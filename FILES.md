# Files and Dirs

`suttapitaka-structure.txt` - description of hierarhy of texts

`sutta-pitaka.sqlite` - database with main data (SQLite)

`make_db_from_text.py` - script makes main table: `segments` with sutra's text from text files

`/sutta-data` - dir with text files (not in git!)

`/backups/sutta-data.zip` - raw text data from https://github.com/suttacentral

`/backups/sutta-pitaka.backup.sqlite.sql` - sql with DB structure (only structure)

`make_table_chapters.sql` - sql-file for making table `chapters_info`

`make_chunks_borders.py` and `make_chunks_content.py` - split chapters by chunks into table `chunks`

`make_embedding.py` - create embedding vectors and place into table `embeddings`

`PIPELINE.md` - A way to reproduce my results

`check_embeddings.py` - Check (delete or show) embeddings if chunks changed

`indexing.py` - library (module) for indexing and search

`true_validated_answers.txt` - True answers, validated by expert

`validate_model.py` - Script for validating the model (with set of questions)
