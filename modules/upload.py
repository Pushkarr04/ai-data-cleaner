import streamlit as st
import pandas as pd
import seaborn as sns
import requests
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=3)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

def show_upload_module():
    # ── Upload Zone ──
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
        <div style="width:4px; height:28px; background:linear-gradient(180deg,#4FACFE,#00F2FE); border-radius:4px;"></div>
        <span style="font-size:1.4rem; font-weight:700; color:#E2E8F0;">Upload Your Dataset</span>
    </div>
    <p style="color:#64748B; font-size:0.88rem; margin:0 0 16px 14px;">
        Supports CSV · XLSX · XLS &nbsp;|&nbsp; Max file size depends on your browser memory
    </p>
    """, unsafe_allow_html=True)

    col_upload, col_sample = st.columns([3, 2])

    with col_upload:
        uploaded_file = st.file_uploader(
            "Drop your file here or click to browse",
            type=["csv", "xlsx", "xls"],
            help="Upload any CSV or Excel file to begin cleaning",
        )

    with col_sample:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.07);
            border-radius:14px; padding:16px 18px; margin-top:4px;">
            <div style="font-weight:700; color:#E2E8F0; margin-bottom:8px; font-size:0.9rem;">
                📦 Quick Start — Sample Datasets
            </div>
        """, unsafe_allow_html=True)
        sample_dataset = st.selectbox(
            "Pick a built-in dataset",
            ["None", "titanic", "tips", "iris", "diamonds", "planets"],
            label_visibility="collapsed"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    df = None

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            _show_upload_success(df, uploaded_file.name)
        except Exception as e:
            st.error(f"❌ Error loading file: {e}")

    elif sample_dataset != "None":
        try:
            df = sns.load_dataset(sample_dataset)
            _show_upload_success(df, sample_dataset)
        except Exception as e:
            st.error(f"❌ Error loading sample dataset: {e}")

    return df


def _show_upload_success(df, name):
    """Show a rich success banner after upload."""
    total_cells = df.shape[0] * df.shape[1]
    missing = df.isnull().sum().sum()
    missing_pct = (missing / total_cells * 100) if total_cells > 0 else 0
    dups = df.duplicated().sum()
    mem_mb = df.memory_usage(deep=True).sum() / 1024**2

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(0,242,254,0.08) 0%, rgba(79,172,254,0.05) 100%);
        border: 1px solid rgba(0,242,254,0.25); border-radius:16px; padding:20px 24px; margin: 16px 0;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
            <span style="font-size:1.4rem;">✅</span>
            <span style="font-size:1.05rem; font-weight:700; color:#E2E8F0;">
                <span style="color:#00F2FE;">{name}</span> loaded successfully!
            </span>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:12px;">
            <div style="background:rgba(0,0,0,0.2); border-radius:10px; padding:10px 16px; flex:1; min-width:100px; text-align:center;">
                <div style="font-size:1.5rem; font-weight:800; color:#00F2FE;">{df.shape[0]:,}</div>
                <div style="color:#64748B; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Rows</div>
            </div>
            <div style="background:rgba(0,0,0,0.2); border-radius:10px; padding:10px 16px; flex:1; min-width:100px; text-align:center;">
                <div style="font-size:1.5rem; font-weight:800; color:#4FACFE;">{df.shape[1]}</div>
                <div style="color:#64748B; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Columns</div>
            </div>
            <div style="background:rgba(0,0,0,0.2); border-radius:10px; padding:10px 16px; flex:1; min-width:100px; text-align:center;">
                <div style="font-size:1.5rem; font-weight:800; color:#F59E0B;">{missing:,}</div>
                <div style="color:#64748B; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Missing ({missing_pct:.1f}%)</div>
            </div>
            <div style="background:rgba(0,0,0,0.2); border-radius:10px; padding:10px 16px; flex:1; min-width:100px; text-align:center;">
                <div style="font-size:1.5rem; font-weight:800; color:#F87171;">{dups:,}</div>
                <div style="color:#64748B; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Duplicates</div>
            </div>
            <div style="background:rgba(0,0,0,0.2); border-radius:10px; padding:10px 16px; flex:1; min-width:100px; text-align:center;">
                <div style="font-size:1.5rem; font-weight:800; color:#A78BFA;">{mem_mb:.2f} MB</div>
                <div style="color:#64748B; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Memory</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
