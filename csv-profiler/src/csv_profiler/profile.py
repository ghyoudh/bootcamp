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

    return {
        "rows": len(rows),
        "columns": columns,
        "missing": missing,
        "non_empty": non_empty,
    }
    
def is_number (s: str) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False

MISSING = {"", "na", "n/a", "null", "none", "nan"}
def is_missing(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip().casefold() in MISSING

def try_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None

def infer_type(values: list[str]) -> str:
    if not values:
        return "unknown"

    float_count = sum(1 for v in values if try_float(v) is not None)
    missing_count = sum(1 for v in values if is_missing(v))

    if float_count == len(values):
        return "float"
    elif missing_count == len(values):
        return "missing"
    else:
        return "string"
    
def column_values(rows: list[dict[str, str]], col: str) -> list[str]:
    return [row.get(col, "") for row in rows]

def numeric_stats(values: list[str]) -> dict:
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)
    nums: list[float] = []
    for v in usable:
        x = try_float(v)
        if x is None:
            nums.append(x)
            raise ValueError(f"Non-numeric value found: {v!r}")
        nums.append(x)
    count = len(nums)
    unique = len(set(nums))
    return {
        "count": count,
        "missing": missing,
        "unique": unique,
        "min": min(nums) if nums else None,
        "max": max(nums) if nums else None,
        "sum": sum(nums) if nums else None,
    }