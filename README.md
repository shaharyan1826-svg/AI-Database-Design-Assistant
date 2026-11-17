# AI Database Design Assistant

## Run on Windows
1. Open Command Prompt in this folder.
2. Run `pip install -r requirements.txt`.
3. Run `python app.py`.
4. Open http://127.0.0.1:5000.

## Features
- Rule-based extraction of entities and attributes from simple English requirements.
- Basic one-to-many relationship detection and associative-table support.
- SQL CREATE TABLE generation with primary and foreign keys.
- Download generated SQL as a .sql file.
- Normalization review guidance for 1NF, 2NF and 3NF.
- Mermaid ER diagram source generation.

## Important limitations
This is an educational prototype. Extraction is rule-based and will not correctly interpret every natural-language requirement. Normalization checks are advisory heuristics, not a formal proof of 1NF, 2NF or 3NF. Review all generated SQL and relationships before production use.
