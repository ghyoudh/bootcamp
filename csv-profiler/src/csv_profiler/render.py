from __future__ import annotations
from pathlib import Path

import json

def md_header(title: str) -> list[str]:
    return [f"# {title}", ""]

def md_table_header() -> list[str]:
    return ["| Column Name | Inferred Type | Non-Null Count | Null Count |"]

def md_table_row(name: str, col: dict, total_rows: int) -> list[str]:
    return [f"| {name} | {col.get('type', 'unknown')} | {col.get('non_null', 0)} | {col.get('null', 0)} |"]

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
    lines.append("## Columns (table)")
    lines.extend(md_table_header())
    for name, col in report["columns"].items():
        lines.extend(md_table_row(name, col, rows))
    lines.append("")
