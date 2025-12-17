import streamlit as st
from io import StringIO
import csv
import pandas as pd

st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")

# ---- Initialize session state ----
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False

if "rows" not in st.session_state:
    st.session_state.rows = None

if "show_preview" not in st.session_state:
    st.session_state.show_preview = True

uploaded = st.file_uploader("Upload a CSV file", type=["csv"])

# ---- Generate report (one time) ----
if uploaded is not None and not st.session_state.report_generated:
    if st.button("Generate Profile Report"):
        text = uploaded.getvalue().decode("utf-8-sig")
        st.session_state.rows = list(csv.DictReader(StringIO(text)))
        st.session_state.report_generated = True

# ---- Display report (no regeneration) ----
if st.session_state.report_generated:
    rows = st.session_state.rows

    st.write("Filename:", uploaded.name)
    st.write("Rows loaded:", len(rows))

    st.session_state.show_preview = st.checkbox(
        "Show CSV Preview",
        value=st.session_state.show_preview
    )

    if st.session_state.show_preview:
        st.write(rows[:5])
    else:
        df = pd.DataFrame(rows[:5])
        st.table(df)

else:
    st.info("Upload a CSV file to begin.")
