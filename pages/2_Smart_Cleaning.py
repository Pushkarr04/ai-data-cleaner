import streamlit as st
import requests
from streamlit_lottie import st_lottie
from modules.ui import PREMIUM_CSS, SIDEBAR_HTML
from modules.cleaner import show_cleaning_options

st.set_page_config(page_title="Smart Cleaning | DataCleaner AI", page_icon="🧹", layout="wide")
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=3)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

with st.sidebar:
    st.markdown(SIDEBAR_HTML, unsafe_allow_html=True)
    st.markdown("---")
    if st.session_state.get('raw_df') is not None:
        df = st.session_state['raw_df']
        st.markdown(f"""
        <div style="background:rgba(0,242,254,0.05); border:1px solid rgba(0,242,254,0.15);
            border-radius:10px; padding:12px; font-size:0.82rem; color:#94A3B8; line-height:2;">
            📐 Rows: <b style="color:#00F2FE">{df.shape[0]:,}</b><br>
            📏 Cols: <b style="color:#00F2FE">{df.shape[1]}</b><br>
            ❓ Missing: <b style="color:#F59E0B">{df.isnull().sum().sum():,}</b><br>
            🗂️ Dups: <b style="color:#F59E0B">{df.duplicated().sum():,}</b>
        </div>
        """, unsafe_allow_html=True)

if st.session_state.get('raw_df') is not None:
    cleaned, logs = show_cleaning_options(st.session_state['raw_df'])
    if cleaned is not None:
        st.session_state['cleaned_df'] = cleaned
        st.session_state['cleaning_logs'] = logs

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
            <div style="width:4px; height:28px; background:linear-gradient(180deg,#22C55E,#4ADE80); border-radius:4px;"></div>
            <span style="font-size:1.2rem; font-weight:700; color:#E2E8F0;">✨ Real-Time Updates</span>
        </div>
        """, unsafe_allow_html=True)

        if logs:
            st.markdown(f"""
            <div style="background:rgba(34,197,94,0.07); border:1px solid rgba(34,197,94,0.2);
                border-radius:14px; padding:18px 22px; margin:12px 0;">
                <div style="font-weight:700; color:#22C55E; margin-bottom:10px;">
                    ✅ {len(logs)} transformation(s) currently active
                </div>
                {"".join([f'<div style=\"color:#94A3B8; font-size:0.83rem; padding:2px 0;\">• {l}</div>' for l in logs])}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No cleaning steps applied yet. Use the options above to start cleaning.")

        st.markdown("""
        <div style="background:rgba(0,242,254,0.04); border:1px solid rgba(0,242,254,0.15);
            border-radius:12px; padding:14px 18px; margin-top:4px;">
            <div style="font-weight:700; color:#00F2FE; font-size:0.9rem; margin-bottom:10px;">
                🔍 Live Preview of Cleaned Dataset
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(cleaned.head(10), use_container_width=True)
        st.markdown(f"<span style='color:#64748B; font-size:0.78rem;'>{len(cleaned):,} rows · {len(cleaned.columns)} columns after cleaning</span>",
                    unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align:center; padding:80px 20px; background:rgba(255,255,255,0.02);
        border:1px dashed rgba(255,255,255,0.08); border-radius:18px; margin-top:40px;">
        <div style="font-size:3.5rem; margin-bottom:16px;">🧹</div>
        <div style="font-size:1.15rem; font-weight:700; color:#E2E8F0; margin-bottom:8px;">No Dataset Loaded</div>
        <div style="color:#64748B; font-size:0.9rem;">Please upload a dataset on the <b>Home</b> page first.</div>
    </div>
    """, unsafe_allow_html=True)
