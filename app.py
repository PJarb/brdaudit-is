import streamlit as st
import pandas as pd
import joblib
from sentence_transformers import SentenceTransformer
from utils.pdf_utils import extract_pdf_to_text
from utils.llm_utils import consolidate_requirements
from utils.predict_utils import predict_requirements

st.set_page_config(page_title="BRD Audit Tool", layout="wide")

st.title("📄 BRD Requirement Audit")

# ---------------------------
# Step 1: Upload PDF
# ---------------------------
uploaded_file = st.file_uploader("Upload BRD PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        raw_text = extract_pdf_to_text(uploaded_file)

    st.success("PDF extracted")

    # ---------------------------
    # Step 2: LLM Consolidation
    # ---------------------------
    if st.button("🔍 Consolidate Requirements"):
        with st.spinner("Running LLM consolidation..."):
            requirements = consolidate_requirements(raw_text)

        df_req = pd.DataFrame(requirements)
        st.subheader("Consolidated Requirements")
        st.dataframe(df_req, use_container_width=True)

        # ---------------------------
        # Step 3: Audit with ML
        # ---------------------------
        if st.button("✅ Run Audit"):
            with st.spinner("Auditing requirements..."):
                result_df = predict_requirements(df_req)

            st.subheader("Audit Result")
            st.dataframe(result_df, use_container_width=True)

            # Summary
            st.subheader("Summary")
            st.bar_chart(result_df["Prediction"].value_counts())

            # Download
            st.download_button(
                "Download Result (CSV)",
                result_df.to_csv(index=False).encode("utf-8"),
                "brd_audit_result.csv",
                "text/csv"
            )
