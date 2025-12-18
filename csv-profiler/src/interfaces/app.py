import streamlit as st
from io import StringIO
import csv, json
import pandas as pd
from src.csv_profiler import profile
from src.csv_profiler import render
from pathlib import Path

st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")
st.caption("Upload CSV → profile → export JSON + Markdown")

st.sidebar.header("Inputs")

rows =0
report = st.session_state.get("report")
# File uploader
uploaded = st.file_uploader("Upload a CSV file", type=["csv"])
show_preview = st.sidebar.checkbox("Show preview", value=True)

# Process uploaded file
if uploaded is not None:
    text = uploaded.getvalue().decode("utf-8-sig")
    rows = list(csv.DictReader(StringIO(text)))

    # Show preview 
    if show_preview:
        st.subheader("Data Preview")
        df = pd.DataFrame(rows[:10])
        st.table(df)

        # Display column details
        st.subheader("Columns Details")
        df_2 = pd.DataFrame.from_dict(report["columns"], orient="index")
        st.dataframe(df_2, use_container_width=True)


    # Generate report button
    if rows is not None:
        if len(rows) > 0:
            if st.button("Generate Report"):
                st.session_state["report"] = profile.basic_profile(rows)
    st.session_state["report"] = profile.basic_profile(rows)

    if report is not None:
        cols =st.columns(2)
        cols[0].metric("Rows", report["summary"]["rows"])
        cols[1].metric("Columns", report["summary"]["columns"])

        with st.expander("Markdown Preview", expanded=False):
            md_content = render.write_markdown(report, "preview.md")
            preview_path = Path("preview.md")
            if preview_path.exists():
                st.markdown(preview_path.read_text(encoding="utf-8"))
            else:
                st.info("No markdown preview available")

        # Export options
        # 1. json
        report_name =st.sidebar.text_input("Report name", value="report")
        json_file = report_name + ".json"
        json_text = json.dumps(report, indent=2, ensure_ascii=False)
        # 2. markdown
        md_file = report_name + ".md"
        md_file_path = Path(md_file)
        render.write_markdown(report, str(md_file_path))
        md_text = md_file_path.read_text(encoding="utf-8")

        c1, c2 = st.columns(2)
        c1.download_button("Download JSON", data= json_text, file_name=json_file)
        c2.download_button("Download Markdown", data= md_text, file_name=md_file)

        # Save report button
        if st.sidebar.button("Save the report"):
            out_dir = Path("output")
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / json_file).write_text(json_text, encoding="utf-8")
            (out_dir / md_file).write_text(md_text, encoding="utf-8")
            st.success(f"Saved to output/{json_file} and output/{md_file}")

else:
    st.info("Upload a CSV file to begin.")
