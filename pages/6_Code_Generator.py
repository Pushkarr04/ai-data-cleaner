import streamlit as st
from modules.ui import PREMIUM_CSS, SIDEBAR_HTML
from modules.code_generator import show_code_generator

st.set_page_config(page_title="Code Generator | DataCleaner AI", page_icon="💻", layout="wide")
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(SIDEBAR_HTML, unsafe_allow_html=True)
    st.markdown("---")
    logs = st.session_state.get('cleaning_logs', [])
    st.markdown(f"""
    <div style="background:rgba(0,242,254,0.05); border:1px solid rgba(0,242,254,0.15);
        border-radius:10px; padding:12px; font-size:0.82rem; color:#94A3B8; line-height:2;">
        💻 Logged Steps: <b style="color:#00F2FE">{len(logs)}</b>
    </div>
    """, unsafe_allow_html=True)

show_code_generator(st.session_state.get('cleaning_logs', []))
