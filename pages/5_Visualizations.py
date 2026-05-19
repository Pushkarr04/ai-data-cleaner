import streamlit as st
from modules.ui import PREMIUM_CSS, SIDEBAR_HTML
from modules.visualize import show_visualizations

st.set_page_config(page_title="Visualizations | DataCleaner AI", page_icon="📊", layout="wide")
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(SIDEBAR_HTML, unsafe_allow_html=True)
    st.markdown("---")
    if st.session_state.get('raw_df') is not None:
        df = st.session_state['raw_df']
        st.markdown(f"""
        <div style="background:rgba(0,242,254,0.05); border:1px solid rgba(0,242,254,0.15);
            border-radius:10px; padding:12px; font-size:0.82rem; color:#94A3B8; line-height:2;">
            📐 Rows: <b style="color:#00F2FE">{df.shape[0]:,}</b><br>
            📏 Cols: <b style="color:#00F2FE">{df.shape[1]}</b>
        </div>
        """, unsafe_allow_html=True)

if st.session_state.get('raw_df') is not None and st.session_state.get('cleaned_df') is not None:
    show_visualizations(st.session_state['raw_df'], st.session_state['cleaned_df'])
else:
    st.markdown("""
    <div style="text-align:center; padding:80px 20px; background:rgba(255,255,255,0.02);
        border:1px dashed rgba(255,255,255,0.08); border-radius:18px; margin-top:40px;">
        <div style="font-size:3.5rem; margin-bottom:16px;">📊</div>
        <div style="font-size:1.15rem; font-weight:700; color:#E2E8F0; margin-bottom:8px;">No Dataset Loaded</div>
        <div style="color:#64748B; font-size:0.9rem;">Please upload a dataset on the <b>Home</b> page first.</div>
    </div>
    """, unsafe_allow_html=True)
