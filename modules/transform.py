import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
from modules.ui import PREMIUM_CSS, section_header

def show_transformation(df):
    st.markdown(PREMIUM_CSS, unsafe_allow_html=True)
    section_header("⚙️", "Data Transformations", "Scale numerics, encode categoricals, and engineer new features.")

    if df is None:
        st.info("Please upload a dataset on the Home page first.")
        return None, []

    transformed_df = df.copy()
    transform_logs = []

    tab1, tab2, tab3 = st.tabs(["📐 Numerical Scaling", "🏷️ Categorical Encoding", "🔧 Feature Engineering"])

    with tab1:
        section_header("📐", "Numerical Scaling")
        num_cols = transformed_df.select_dtypes(include=['number']).columns.tolist()

        if not num_cols:
            st.info("No numerical columns available for scaling.")
        else:
            scale_cols = st.multiselect("Select columns to scale", num_cols, key="scale_cols")
            scale_method = st.radio("Scaling Method", [
                "Min-Max Normalization (0–1)",
                "Standardization (Z-score / Mean=0, Std=1)"
            ], horizontal=True, key="scale_method")

            if scale_cols:
                if st.button("⚡ Apply Scaling", key="apply_scale"):
                    if "Min-Max" in scale_method:
                        scaler = MinMaxScaler()
                        transformed_df[scale_cols] = scaler.fit_transform(transformed_df[scale_cols])
                        transform_logs.append(f"Applied Min-Max Normalization to {len(scale_cols)} columns.")
                    else:
                        scaler = StandardScaler()
                        transformed_df[scale_cols] = scaler.fit_transform(transformed_df[scale_cols])
                        transform_logs.append(f"Applied Standardization to {len(scale_cols)} columns.")

                    st.markdown(f"""
                    <div style="background:rgba(34,197,94,0.08); border:1px solid rgba(34,197,94,0.25);
                        border-radius:12px; padding:14px 18px; margin-top:12px;">
                        ✅ <b style="color:#22C55E;">Scaling applied</b> — {len(scale_cols)} column(s) transformed.
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("""
                    <div style="background:rgba(0,242,254,0.04); border:1px solid rgba(0,242,254,0.15);
                        border-radius:10px; padding:10px 16px; margin-top:10px;">
                        <div style="font-weight:700; color:#00F2FE; font-size:0.85rem; margin-bottom:8px;">
                            🔍 Preview Scaled Columns
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.dataframe(transformed_df[scale_cols].head(10), use_container_width=True)
            else:
                st.info("Select at least one column above to begin scaling.")

    with tab2:
        section_header("🏷️", "Categorical Encoding")
        cat_cols = transformed_df.select_dtypes(include=['object', 'category']).columns.tolist()

        if not cat_cols:
            st.info("No categorical columns available for encoding.")
        else:
            encode_cols = st.multiselect("Select columns to encode", cat_cols, key="encode_cols")
            encode_method = st.radio("Encoding Method", [
                "Label Encoding (Ordinal integers)",
                "One-Hot Encoding (Binary dummy columns)"
            ], horizontal=True, key="encode_method")

            if encode_cols:
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Before encoding:**")
                    st.dataframe(transformed_df[encode_cols].head(5), use_container_width=True)

                if st.button("⚡ Apply Encoding", key="apply_encode"):
                    if "Label" in encode_method:
                        le = LabelEncoder()
                        for col in encode_cols:
                            transformed_df[col] = le.fit_transform(transformed_df[col].astype(str))
                        transform_logs.append(f"Applied Label Encoding to {len(encode_cols)} columns.")
                    else:
                        transformed_df = pd.get_dummies(transformed_df, columns=encode_cols, drop_first=True)
                        transform_logs.append(f"Applied One-Hot Encoding to {len(encode_cols)} columns.")

                    st.markdown(f"""
                    <div style="background:rgba(34,197,94,0.08); border:1px solid rgba(34,197,94,0.25);
                        border-radius:12px; padding:14px 18px; margin-top:12px;">
                        ✅ <b style="color:#22C55E;">Encoding applied</b> — {len(encode_cols)} column(s) encoded.
                    </div>
                    """, unsafe_allow_html=True)

                    with c2:
                        st.markdown("**After encoding:**")
                        preview_cols = [c for c in encode_cols if c in transformed_df.columns]
                        if preview_cols:
                            st.dataframe(transformed_df[preview_cols].head(5), use_container_width=True)
                        else:
                            st.dataframe(transformed_df.head(5), use_container_width=True)
            else:
                st.info("Select at least one column above to begin encoding.")

    with tab3:
        section_header("🔧", "Feature Engineering")
        num_cols2 = transformed_df.select_dtypes(include='number').columns.tolist()

        if len(num_cols2) < 2:
            st.info("Need at least 2 numeric columns to engineer features.")
        else:
            st.markdown("<span style='color:#94A3B8; font-size:0.88rem;'>Create a new column by combining two existing numeric columns.</span>", unsafe_allow_html=True)
            fc1, fc2, fc3 = st.columns(3)
            with fc1:
                feat_col1 = st.selectbox("Column A", num_cols2, key="feat_col1")
            with fc2:
                operation = st.selectbox("Operation", ["Add (+)", "Subtract (−)", "Multiply (×)", "Divide (÷)"], key="feat_op")
            with fc3:
                feat_col2 = st.selectbox("Column B", num_cols2, key="feat_col2")

            new_col_name = st.text_input("New column name", value=f"{feat_col1}_{feat_col2}_engineered", key="feat_new_name")

            if st.button("⚡ Create Feature", key="apply_feat"):
                try:
                    if "Add" in operation:
                        transformed_df[new_col_name] = transformed_df[feat_col1] + transformed_df[feat_col2]
                    elif "Subtract" in operation:
                        transformed_df[new_col_name] = transformed_df[feat_col1] - transformed_df[feat_col2]
                    elif "Multiply" in operation:
                        transformed_df[new_col_name] = transformed_df[feat_col1] * transformed_df[feat_col2]
                    elif "Divide" in operation:
                        transformed_df[new_col_name] = transformed_df[feat_col1] / transformed_df[feat_col2].replace(0, np.nan)

                    transform_logs.append(f"Engineered new feature '{new_col_name}'.")
                    st.markdown(f"""
                    <div style="background:rgba(34,197,94,0.08); border:1px solid rgba(34,197,94,0.25);
                        border-radius:12px; padding:14px 18px; margin-top:12px;">
                        ✅ <b style="color:#22C55E;">Feature created:</b> '{new_col_name}' added to the dataset.
                    </div>
                    """, unsafe_allow_html=True)
                    st.dataframe(transformed_df[[feat_col1, feat_col2, new_col_name]].head(10), use_container_width=True)
                except Exception as e:
                    st.error(f"Feature engineering failed: {e}")

    if transform_logs:
        st.markdown("<br>", unsafe_allow_html=True)
        section_header("📋", "Applied Transformations")
        for log in transform_logs:
            st.markdown(f"<div style='color:#94A3B8; font-size:0.87rem; padding:4px 0;'>✅ {log}</div>", unsafe_allow_html=True)

    return transformed_df, transform_logs
