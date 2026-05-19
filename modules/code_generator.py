import streamlit as st
from modules.ui import PREMIUM_CSS, section_header

def show_code_generator(logs):
    st.markdown(PREMIUM_CSS, unsafe_allow_html=True)
    section_header("💻", "Python Code Generator",
                   "Automatically generate a reproducible Python script based on every cleaning step you applied in the UI.")

    if not logs:
        st.markdown("""
        <div style="text-align:center; padding:60px 20px; background:rgba(255,255,255,0.02);
            border:1px dashed rgba(255,255,255,0.1); border-radius:18px;">
            <div style="font-size:3.5rem; margin-bottom:16px;">💻</div>
            <div style="font-size:1.1rem; font-weight:700; color:#E2E8F0; margin-bottom:8px;">
                No actions logged yet
            </div>
            <div style="color:#64748B; font-size:0.88rem;">
                Go to <b>Smart Cleaning</b>, <b>Transformations</b>, or <b>Data Privacy</b> and
                apply some operations — they will appear as runnable Python code here.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    code = [
        "import pandas as pd",
        "import numpy as np",
        "from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder",
        "from sklearn.impute import KNNImputer",
        "",
        "# ─────────────────────────────────────────",
        "# DataCleaner AI — Auto-Generated Pipeline",
        "# ─────────────────────────────────────────",
        "",
        "df = pd.read_csv('your_dataset.csv')  # 👈 Replace with your file path",
        "print(f'Loaded dataset: {df.shape[0]} rows × {df.shape[1]} columns')",
        "",
        "# ── Cleaning Steps ──"
    ]

    for log in logs:
        if "Filled missing values in" in log:
            col = log.split("'")[1]
            if "Mean"    in log: code.append(f"df['{col}'].fillna(df['{col}'].mean(), inplace=True)")
            elif "Median" in log: code.append(f"df['{col}'].fillna(df['{col}'].median(), inplace=True)")
            elif "Mode"   in log: code.append(f"df['{col}'].fillna(df['{col}'].mode()[0], inplace=True)")
            elif "'Unknown'" in log: code.append(f"df['{col}'].fillna('Unknown', inplace=True)")
        elif "KNN Imputation" in log:
            col = log.split("'")[1]
            code.append(f"# KNN Imputation on '{col}'")
            code.append("num_df = df.select_dtypes(include=['number'])")
            code.append("imputer = KNNImputer(n_neighbors=5)")
            code.append("df[num_df.columns] = imputer.fit_transform(num_df)")
        elif "Dropped rows with missing" in log:
            col = log.split("'")[1]
            code.append(f"df.dropna(subset=['{col}'], inplace=True)")
        elif "duplicate rows" in log:
            code.append("df.drop_duplicates(inplace=True)")
        elif "Converted column" in log and "numeric" in log:
            col = log.split("'")[1]
            code.append(f"df['{col}'] = pd.to_numeric(df['{col}'], errors='coerce')")
        elif "Capped outliers" in log:
            col = log.split("'")[1]
            code.append(f"\n# IQR Outlier Capping — {col}")
            code.append(f"Q1 = df['{col}'].quantile(0.25)")
            code.append(f"Q3 = df['{col}'].quantile(0.75)")
            code.append("IQR = Q3 - Q1")
            code.append(f"df['{col}'] = df['{col}'].clip(lower=Q1 - 1.5*IQR, upper=Q3 + 1.5*IQR)")
        elif "Removed" in log and "outliers" in log:
            col = log.split("'")[1]
            code.append(f"Q1 = df['{col}'].quantile(0.25); Q3 = df['{col}'].quantile(0.75); IQR = Q3 - Q1")
            code.append(f"df = df[(df['{col}'] >= Q1 - 1.5*IQR) & (df['{col}'] <= Q3 + 1.5*IQR)]")
        elif "Min-Max Normalization" in log:
            code.append("\n# Min-Max Normalization")
            code.append("scaler = MinMaxScaler()")
            code.append("num_cols = df.select_dtypes(include=['number']).columns")
            code.append("df[num_cols] = scaler.fit_transform(df[num_cols])")
        elif "Standardization" in log:
            code.append("\n# Z-score Standardization")
            code.append("scaler = StandardScaler()")
            code.append("num_cols = df.select_dtypes(include=['number']).columns")
            code.append("df[num_cols] = scaler.fit_transform(df[num_cols])")
        elif "Label Encoding" in log:
            code.append("le = LabelEncoder()")
            code.append("for col in df.select_dtypes(include='object').columns:")
            code.append("    df[col] = le.fit_transform(df[col].astype(str))")
        elif "One-Hot Encoding" in log:
            code.append("df = pd.get_dummies(df, drop_first=True)")
        elif "Text cleaning" in log:
            col = log.split("'")[1]
            code.append(f"df['{col}'] = df['{col}'].str.lower().str.replace(r'<[^>]*>', '', regex=True).str.replace(r'http\\S+', '', regex=True)")
        elif "Date/Time features" in log:
            col = log.split("'")[1]
            code.append(f"df['{col}'] = pd.to_datetime(df['{col}'], errors='coerce')")
            code.append(f"df['{col}_Year'] = df['{col}'].dt.year")
            code.append(f"df['{col}_Month'] = df['{col}'].dt.month")
            code.append(f"df['{col}_Day'] = df['{col}'].dt.day")
        elif "SHA-256 hashed" in log:
            col = log.split("'")[1]
            code.append(f"import hashlib")
            code.append(f"df['{col}'] = df['{col}'].astype(str).apply(lambda x: hashlib.sha256(x.encode()).hexdigest())")
        elif "Dropped PII column" in log:
            col = log.split("'")[1]
            code.append(f"df.drop(columns=['{col}'], inplace=True)")
        elif "Engineered new feature" in log:
            col = log.split("'")[1]
            code.append(f"# Feature '{col}' was engineered in the UI — replicate the logic here")

    code += ["", "# ── Export ──",
             "df.to_csv('cleaned_dataset.csv', index=False)",
             "print(f'Done! Cleaned dataset saved: {df.shape[0]} rows × {df.shape[1]} columns')"]

    code_str = "\n".join(code)

    # ── Applied Steps Log ──
    st.markdown(f"""
    <div style="background:rgba(0,242,254,0.05); border:1px solid rgba(0,242,254,0.15);
        border-radius:14px; padding:18px 22px; margin-bottom:20px;">
        <div style="font-weight:700; color:#00F2FE; margin-bottom:10px;">
            📋 {len(logs)} Cleaning Step(s) Recorded
        </div>
        {"".join([f'<div style="color:#94A3B8; font-size:0.83rem; padding:2px 0;">✅ {l}</div>' for l in logs])}
    </div>
    """, unsafe_allow_html=True)

    # ── Code block ──
    st.code(code_str, language='python')

    st.download_button(
        label="⬇️ Download Pipeline Script (.py)",
        data=code_str,
        file_name="datacleaner_pipeline.py",
        mime="text/plain",
        type="primary",
        use_container_width=True
    )
