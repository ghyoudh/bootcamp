def basic_profile(rows: list[dict[str, str]]) -> dict:
    if not rows:
     return {"rows": 0, "columns": {}, "notes": ["Empty dataset"]}

    columns = list(rows[0].keys())
    missing = {c: 0 for c in columns}
    non_empty = {c: 0 for c in columns}

    for row in rows:
        for c in columns:
            v = (row.get(c) or "").strip()
            if v == "":
                missing[c] += 1
            else:
                non_empty[c] += 1
    
def is_number (s: str) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False