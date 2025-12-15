from __future__ import annotations
from pathlib import Path

import json

def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(json.dumps(report, indent=2, ensure_ascii=False)+ "\n", encoding="utf-8")

def write_markdown(report: dict, path: str | Path) -> None:
    
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    columns = report.get("columns", [])
    missing = report.get("missing", {})
    lines: list[str] = []
    lines.append(f"# CSV Profile Report\n\n")
    lines.append(f"- Rows: **{report.get('rows', 0)}**")
