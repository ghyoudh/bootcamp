import typer
from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import write_markdown, write_json

app = typer.Typer()

@app.command()
def profile(csv_path: str, output: str = "output"):
    rows = read_csv_rows(csv_path)
    report = basic_profile(rows)
    write_json(report, f"{output}/report.json")
    write_markdown(report, f"{output}/report.md")
    typer.echo(f"Reports written to {output}")

