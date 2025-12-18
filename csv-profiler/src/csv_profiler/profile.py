def basic_profile(rows: list[dict[str, str]]) -> dict:
    cols = get_columns(rows)
    report = {
        "summary": {
            "rows": len(rows),
            "columns": len(cols),
            "column_names": cols,
        },
        "columns": {},
    }

    for col in cols:
        values = column_values(rows, col)
        typ = infer_type(values)

        # Count nulls and non-nulls
        non_null_values = [v for v in values if v is not None and v != ""]
        null_count = len(values) - len(non_null_values)
        non_null_count = len(non_null_values)

        # Unique values
        unique_values = set(non_null_values)

        # Column report
        col_report = {
            "type": typ,
            "non_null": non_null_count,
            "null": null_count,
            "unique": len(unique_values),
        }

        # Add simple stats if numeric
        if typ in ("int", "float"):
            try:
                numeric_values = [float(v) for v in non_null_values]
                col_report.update({
                    "min": min(numeric_values),
                    "max": max(numeric_values),
                })
            except ValueError:
                # If conversion fails, skip stats
                pass

        # Save column profile
        report["columns"][col] = col_report

    return report


def get_columns(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return []
    return list(rows[0].keys())

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

    # Filter out missing values
    non_missing = [v for v in values if not is_missing(v)]
    if not non_missing:
        return "missing"

    # Try integer detection
    int_count = sum(1 for v in non_missing if v.isdigit())
    if int_count == len(non_missing):
        return "int"

    # Try float detection
    float_count = sum(1 for v in non_missing if try_float(v) is not None)
    if float_count == len(non_missing):
        return "float"

    # Default fallback
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

def text_stats(values: list[str], top_k: int = 5) -> dict:
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)
    counts: dict[str, int] = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1
    top_items = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    top = [{"value": v, "count": c} for v, c in top_items]
    
    return {"count": len(usable),"missing": missing, "unique": len(counts), "top": top[:top_k]}
