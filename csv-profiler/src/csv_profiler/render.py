from __future__ import annotations
from pathlib import Path

import json

def md_header(title: str) -> list[str]:
    return [f"# {title}", ""]

def md_table_header() -> list[str]:
    return ["| Column Name | Inferred Type | Non-Null Count | Null Count |", "| --- | --- | --- | --- |"]

def md_table_row(name: str, col: dict) -> list[str]:
    col_type = col.get('type', 'unknown')
    non_null = col.get('non_null', 0)
    null = col.get('null', 0)
    return [f"| {name} | {col_type} | {non_null} | {null} |"]

def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(json.dumps(report, indent=2, ensure_ascii=False)+ "\n", encoding="utf-8")

def write_markdown(report: dict, path: str | Path) -> None:

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    rows = report["summary"]["rows"]

    lines: list[str] = []
    lines.extend(md_header("data/sample.csv"))
    lines.append("## Summary")
    lines.append(f"- Rows: {rows:,}")
    lines.append("")
    lines.append(f"- Columns: {report['summary']['columns']:,}")
    lines.append("")
    lines.append("## Columns (table)")
    lines.extend(md_table_header())
    for name, col in report["columns"].items():
        lines.extend(md_table_row(name, col))
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
