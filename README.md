# 🧠 AI Database Design Assistant

**An intelligent database schema generator that converts natural-language requirements into SQL tables, relationships and database design suggestions.**

<p align="center">

**Python · Flask · SQL · HTML/CSS · NLP**

</p>

---

## 📌 About the Project

The **AI Database Design Assistant** is a web-based application developed as part of an AI & Data Science Internship project.

It helps users simplify database design by converting written requirements into a structured database schema.

Users enter their requirements in simple English, and the application identifies entities, attributes and basic relationships before generating SQL statements.

## 🎯 Project Objectives

- Simplify the database design process.
- Extract entities and attributes from written requirements.
- Identify basic relationships between database tables.
- Generate SQL `CREATE TABLE` statements.
- Suggest suitable data types.
- Provide database normalization review guidance.
- Generate ER diagram code.

## ✨ Key Features

| Feature | Description |
|---|---|
| Requirement Analysis | Accepts natural-language input |
| Entity Extraction | Identifies database entities |
| Attribute Extraction | Identifies table columns |
| Relationship Detection | Detects basic table relationships |
| SQL Generation | Generates SQL table definitions |
| Data Type Suggestions | Suggests appropriate column types |
| Normalization Review | Provides 1NF, 2NF and 3NF guidance |
| ER Diagram | Generates Mermaid diagram code |
| SQL Export | Downloads generated SQL |

## 🛠️ Technologies Used

- **Python** – Application logic
- **Flask** – Web framework
- **HTML & CSS** – User interface
- **SQL** – Database schema generation
- **SQLAlchemy** – Database technology dependency
- **Mermaid** – ER diagram representation

## 📂 Project Structure

```text
AI-Database-Design-Assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── sample_requirements.txt
│
├── templates/
│   └── index.html
│
└── tests/
    └── test_schema.py
```

## ⚙️ Installation and Setup

**Step 1: Clone the repository**

```bash
git clone https://github.com/shaharyan1826-svg/AI-Database-Design-Assistant.git
```

**Step 2: Open the project folder**

```bash
cd AI-Database-Design-Assistant
```

**Step 3: Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 4: Run the application**

```bash
python app.py
```

**Step 5: Open in your browser**

Visit:

http://127.0.0.1:5000

## 💡 Example Usage

**Input Requirements:**

A Student has name, email and age. A Course has title and description. A Student enrolls in many Courses through Enrollment.

**Generated Database Tables:**

- Student
- Course
- Enrollment

**Generated SQL Example:**

```sql
CREATE TABLE student (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    age INTEGER
);
```

The application also generates the Course and Enrollment tables, including the detected foreign-key relationships.

## 🧪 Testing

Run the automated tests:

```bash
python -m unittest discover -s tests -v
```

**Current test result:** 1 automated test passed.

## ⚠️ Limitations

- Natural-language extraction currently uses rule-based techniques.
- Complex requirements may need manual correction.
- Normalization results are advisory, not formal verification.
- Generated database schemas should be reviewed before production use.

## 🚀 Future Enhancements

- Advanced NLP using spaCy.
- More accurate relationship detection.
- Formal database normalization analysis.
- Index and query performance recommendations.
- Interactive ER diagram visualization.
- Additional database export formats.

## 👨‍💻 Project Information

**Project:** AI Database Design Assistant  
**Task ID:** AI-PR-007  
**Domain:** Artificial Intelligence & Data Science  
**Author:** Aryan Shah  
**Project Type:** Internship Project

---

*This project demonstrates how natural-language processing techniques and Python can help simplify relational database design.*
