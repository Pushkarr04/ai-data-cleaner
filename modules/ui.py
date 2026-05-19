PREMIUM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

/* ── Font — scoped to avoid overriding Streamlit icon fonts ── */
body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
}
p, li, label, input, textarea, button, select,
[data-testid="stMarkdownContainer"],
[data-testid="stText"],
[data-testid="stCaptionContainer"],
[data-baseweb="typography"],
.stTextInput input,
.stSelectbox label,
.stMultiSelect label,
.stRadio label,
.stCheckbox label {
    font-family: 'Outfit', sans-serif !important;
}
/* Preserve Streamlit's internal icon fonts — stops arrow_right text bleed-through */
[data-testid="stExpander"] summary *,
[data-testid="stExpander"] [data-testid="stExpanderToggleIcon"],
[class*="Icon"], [class*="icon"],
.material-icons {
    font-family: inherit !important;
}

/* ── Background ── */
.stApp {
    background: radial-gradient(ellipse at 20% 20%, #0d1b3e 0%, #0A0F1C 60%, #050810 100%);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(13,27,62,0.97) 0%, rgba(10,15,28,0.97) 100%) !important;
    border-right: 1px solid rgba(0,242,254,0.12) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Buttons ── */
.stButton > button {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600;
    border-radius: 10px !important;
    border: 1.5px solid rgba(0,242,254,0.4) !important;
    background: rgba(0,242,254,0.05) !important;
    color: #E2E8F0 !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0.3px;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(0,242,254,0.35) !important;
    border-color: #00F2FE !important;
    color: #00F2FE !important;
    background: rgba(0,242,254,0.1) !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(0,242,254,0.15);
    border-radius: 16px;
    padding: 20px 24px !important;
    transition: transform 0.2s, box-shadow 0.2s;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,242,254,0.12);
}
[data-testid="stMetricValue"] {
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    color: #00F2FE !important;
    /* NO -webkit-text-fill-color here — causes overlap */
}
[data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
    color: #94A3B8 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 6px;
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-weight: 600;
    color: #94A3B8 !important;
    transition: all 0.2s;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: rgba(0,242,254,0.15) !important;
    color: #00F2FE !important;
    box-shadow: 0 0 15px rgba(0,242,254,0.2);
}

/* ── Expander ── */
[data-testid="stExpander"] {
    border: 1px solid rgba(0,242,254,0.12) !important;
    border-radius: 12px !important;
    background: rgba(255,255,255,0.02) !important;
}

/* ── File Uploader ── */
[data-testid="stFileUploader"] {
    border: 2px dashed rgba(0,242,254,0.3) !important;
    border-radius: 16px !important;
    background: rgba(0,242,254,0.03) !important;
}

/* ── Selectbox ── */
[data-baseweb="select"] > div {
    border-radius: 10px !important;
    border-color: rgba(0,242,254,0.25) !important;
    background: rgba(10,15,28,0.8) !important;
}

/* ── Input fields ── */
[data-baseweb="input"] > div {
    border-radius: 10px !important;
    border-color: rgba(0,242,254,0.2) !important;
    background: rgba(10,15,28,0.8) !important;
}

/* ── Radio / checkbox labels — keep readable ── */
[data-testid="stRadio"] label,
[data-testid="stCheckbox"] label {
    color: #CBD5E1 !important;
    font-size: 0.9rem !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,242,254,0.1);
    border-radius: 12px;
    overflow: hidden;
}

/* ── Alert/Info boxes ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
}

/* ── Multiselect tags ── */
[data-baseweb="tag"] {
    background: rgba(0,242,254,0.15) !important;
    border-radius: 6px !important;
}
</style>
"""


SIDEBAR_HTML = """
<div style="text-align:center; padding:12px 0 20px 0;">
    <div style="font-size:2.2rem;">✨</div>
    <div style="font-size:1.3rem; font-weight:800; color:#00F2FE; letter-spacing:0.5px;">DataCleaner AI</div>
    <div style="font-size:0.72rem; color:#64748B; letter-spacing:2px; text-transform:uppercase; margin-top:4px;">
        Enterprise v3.0
    </div>
</div>
"""

def section_header(icon: str, title: str, subtitle: str = ""):
    import streamlit as st
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:{'4px' if subtitle else '16px'};">
        <div style="width:4px; height:28px; background:linear-gradient(180deg,#4FACFE,#00F2FE); border-radius:4px;"></div>
        <span style="font-size:1.4rem; font-weight:700; color:#E2E8F0;">{icon} {title}</span>
    </div>
    {"<p style='color:#64748B; font-size:0.88rem; margin:0 0 18px 14px;'>" + subtitle + "</p>" if subtitle else ""}
    """, unsafe_allow_html=True)

def stat_card(icon, label, value, color="#00F2FE"):
    return f"""
    <div style="background:rgba(0,0,0,0.2); border:1px solid rgba(255,255,255,0.06); border-radius:12px;
        padding:14px 18px; text-align:center; flex:1; min-width:110px;">
        <div style="font-size:1.1rem; margin-bottom:4px;">{icon}</div>
        <div style="font-size:1.5rem; font-weight:800; color:{color};">{value}</div>
        <div style="color:#64748B; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px;">{label}</div>
    </div>
    """

def info_card(content: str, color: str = "#00F2FE"):
    return f"""
    <div style="background:rgba(255,255,255,0.02); border:1px solid rgba({color},0.15);
        border-radius:14px; padding:18px 22px; margin:10px 0; color:#E2E8F0; line-height:1.8;">
        {content}
    </div>
    """
