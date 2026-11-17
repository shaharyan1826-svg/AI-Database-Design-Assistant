import re
from flask import Flask, render_template, request, Response

app = Flask(__name__)

def clean_name(value):
    value = re.sub(r"[^a-zA-Z0-9_ ]+", "", value.strip().lower())
    value = re.sub(r"\s+", "_", value)
    if value.endswith("ies") and len(value) > 4:
        value = value[:-3] + "y"
    elif value.endswith("s") and not value.endswith(("ss", "us")) and len(value) > 3:
        value = value[:-1]
    return value.strip("_")

def split_attributes(raw):
    raw = re.sub(r"\b(and|with|including)\b", ",", raw, flags=re.I)
    result = []
    for part in re.split(r",|;", raw):
        part = re.sub(r"\b(a|an|the|each|unique)\b", "", part, flags=re.I).strip()
        match = re.search(r"[a-zA-Z][a-zA-Z0-9_]*$", part)
        if match:
            item = clean_name(match.group(0))
            if item and item not in result:
                result.append(item)
    return result

def infer_type(attribute):
    name = attribute.lower()
    if any(x in name for x in ("date", "time")):
        return "DATETIME"
    if any(x in name for x in ("price", "amount", "salary", "score")):
        return "DECIMAL(10,2)"
    if any(x in name for x in ("age", "quantity", "count", "year", "grade")):
        return "INTEGER"
    if name.startswith("is_") or name in {"active", "is_paid"}:
        return "BOOLEAN"
    return "VARCHAR(255)"

def build_schema(requirements):
    entities, attrs = [], {}

    # Extract entity attributes from sentences such as "A Student has name, email and age."
    for match in re.finditer(
        r"\b(?:a|an|the)?\s*([A-Z][A-Za-z_]*)\s+(?:has|have|contains|stores)\s+([^.;\n]+)",
        requirements
    ):
        entity = clean_name(match.group(1))
        if entity and entity not in entities:
            entities.append(entity)
        attrs.setdefault(entity, []).extend(split_attributes(match.group(2)))

    # Explicit entity/table lists.
    for group in re.findall(r"(?:entities|tables)\s+(?:are|include|:)\s+([^.;\n]+)", requirements, re.I):
        group = re.sub(r"\band\b", ",", group, flags=re.I)
        for raw in group.split(","):
            entity = clean_name(raw)
            if entity:
                if entity not in entities:
                    entities.append(entity)
                attrs.setdefault(entity, [])

    # Capture associative entities named after "through".
    for raw in re.findall(r"\bthrough\s+([A-Z][A-Za-z_]*)", requirements):
        entity = clean_name(raw)
        if entity:
            if entity not in entities:
                entities.append(entity)
            attrs.setdefault(entity, [])

    entities = list(dict.fromkeys(entities))
    if not entities:
        entities = ["student", "course", "enrollment"]
        attrs = {
            "student": ["name", "email", "age"],
            "course": ["title", "description"],
            "enrollment": ["enrollment_date", "status"]
        }

    for entity in entities:
        attrs.setdefault(entity, [])
        attrs[entity] = [a for a in dict.fromkeys(attrs[entity]) if a != entity]

    relationships = []
    # Detect associative entity pattern: "Student ... Courses through Enrollment".
    for associative in entities:
        pattern = r"\b([A-Za-z]+)\b.{0,100}\b([A-Za-z]+)s?\b.{0,40}\bthrough\s+" + re.escape(associative) + r"\b"
        for sentence in re.split(r"[.!?]", requirements):
            if re.search(r"\bthrough\s+" + re.escape(associative) + r"\b", sentence, re.I):
                candidates = [e for e in entities if e != associative and re.search(r"\b" + re.escape(e) + r"s?\b", sentence, re.I)]
                if len(candidates) >= 2:
                    relationships.extend([
                        {"from": candidates[0], "to": associative, "type": "one-to-many"},
                        {"from": candidates[1], "to": associative, "type": "one-to-many"}
                    ])

    # Simple direct one-to-many phrases.
    lower = requirements.lower()
    for sentence in re.split(r"[.!?]", lower):
        for parent in entities:
            for child in entities:
                if parent != child and re.search(
                    r"\b" + re.escape(parent) + r"s?\b.{0,55}\b(has many|contains|includes|owns)\b.{0,45}\b" + re.escape(child) + r"s?\b",
                    sentence
                ):
                    relationships.append({"from": parent, "to": child, "type": "one-to-many"})

    unique, seen = [], set()
    for rel in relationships:
        key = (rel["from"], rel["to"], rel["type"])
        if key not in seen:
            seen.add(key)
            unique.append(rel)
    relationships = unique

    tables = {}
    for entity in entities:
        columns = [("id", "INTEGER PRIMARY KEY")]
        for attribute in attrs[entity]:
            if attribute != "id":
                columns.append((attribute, infer_type(attribute)))
        tables[entity] = columns

    for rel in relationships:
        parent, child = rel["from"], rel["to"]
        fk = parent + "_id"
        if fk not in [c[0] for c in tables[child]]:
            tables[child].append((fk, f"INTEGER REFERENCES {parent}(id)"))

    sql_parts = []
    for table, columns in tables.items():
        defs = [f"    {name} {datatype}" for name, datatype in columns]
        sql_parts.append(f"CREATE TABLE {table} (\n" + ",\n".join(defs) + "\n);")
    sql_code = "\n\n".join(sql_parts)

    # Heuristic review: flag likely repeating groups / list-like column names.
    normalization = [
        {"level": "1NF", "status": "Review", "detail": "Columns are generated as single values. Confirm that no field stores comma-separated lists or repeating groups."},
        {"level": "2NF", "status": "Review", "detail": "All generated tables use a single-column primary key. Check that every non-key attribute depends on the whole key."},
        {"level": "3NF", "status": "Review", "detail": "Check for transitive dependencies between non-key attributes; move independently dependent facts into separate tables."}
    ]
    warnings = []
    for entity, columns in tables.items():
        for name, datatype in columns:
            if any(word in name for word in ("list", "items", "all_", "multiple_")):
                warnings.append(f"Review {entity}.{name}: this name may represent a repeating group.")
    if not warnings:
        warnings.append("No obvious repeating-group column names were detected. This does not prove the schema is fully normalized.")

    # Mermaid ER diagram text, useful in Markdown Mermaid viewers.
    mermaid = ["erDiagram"]
    for table, columns in tables.items():
        mermaid.append(f"    {table.upper()} {{")
        for name, datatype in columns:
            dtype = "int" if "INTEGER" in datatype else "string"
            mermaid.append(f"        {dtype} {name}")
        mermaid.append("    }")
    for rel in relationships:
        mermaid.append(f"    {rel['from'].upper()} ||--o{{ {rel['to'].upper()} : relates_to")

    return {
        "entities": entities, "attributes": attrs, "relationships": relationships,
        "tables": tables, "sql": sql_code, "mermaid": "\n".join(mermaid),
        "normalization": normalization, "warnings": warnings
    }

@app.route("/", methods=["GET", "POST"])
def index():
    result, requirements = None, ""
    if request.method == "POST":
        requirements = request.form.get("requirements", "").strip()
        if requirements:
            result = build_schema(requirements)
    return render_template("index.html", result=result, requirements=requirements)

@app.route("/download-sql", methods=["POST"])
def download_sql():
    requirements = request.form.get("requirements", "").strip()
    if not requirements:
        return Response("No requirements supplied.", status=400)
    result = build_schema(requirements)
    return Response(
        result["sql"],
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment; filename=database_schema.sql"}
    )

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)