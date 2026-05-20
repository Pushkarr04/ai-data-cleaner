import streamlit as st
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="DataCleaner AI — Home",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');
body, [class*="css"] { font-family: 'Outfit', sans-serif !important; }
p, li, label, input, textarea, button, select,
[data-testid="stMarkdownContainer"], [data-testid="stText"],
[data-baseweb="typography"], .stTextInput input,
.stRadio label, .stCheckbox label, .stSelectbox label, .stMultiSelect label {
    font-family: 'Outfit', sans-serif !important;
}
[class*="Icon"], [class*="icon"], .material-icons { font-family: inherit !important; }

.stApp {
    background: radial-gradient(ellipse at 15% 15%, #0d1b3e 0%, #0A0F1C 55%, #050810 100%);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(13,27,62,0.97) 0%, rgba(10,15,28,0.97) 100%) !important;
    border-right: 1px solid rgba(0,242,254,0.12) !important;
}
[data-testid="stSidebarNav"] a { border-radius: 10px; transition: all 0.2s ease; }
[data-testid="stSidebarNav"] a:hover {
    background: rgba(0,242,254,0.08) !important; padding-left: 12px;
}
#MainMenu, footer { visibility: hidden; }
[data-testid="stSidebarCollapse"] {
    background-color: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 8px !important;
    color: #E2E8F0 !important;
    transition: all 0.2s ease-in-out !important;
}
[data-testid="stSidebarCollapse"]:hover {
    background-color: rgba(0, 242, 254, 0.1) !important;
    border-color: rgba(0, 242, 254, 0.4) !important;
    color: #00F2FE !important;
}
.stButton > button {
    font-family: 'Outfit', sans-serif !important; font-weight: 600;
    border-radius: 10px !important; border: 1.5px solid rgba(0,242,254,0.4) !important;
    background: rgba(0,242,254,0.05) !important; color: #E2E8F0 !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(0,242,254,0.35) !important;
    border-color: #00F2FE !important; color: #00F2FE !important;
    background: rgba(0,242,254,0.1) !important;
}
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
@keyframes fadeInUp { from{opacity:0;transform:translateY(30px)} to{opacity:1;transform:translateY(0)} }
@keyframes shimmer {
    0%{background-position:-200% center}
    100%{background-position:200% center}
}
.float-anim { animation: float 4s ease-in-out infinite; display:inline-block; }
.fade-up { animation: fadeInUp 0.8s ease both; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ──
for key, default in [('raw_df', None), ('cleaned_df', None), ('cleaning_logs', [])]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:20px 0 24px 0;">
        <div style="font-size:3rem;" class="float-anim">✨</div>
        <div style="font-size:1.4rem; font-weight:800; color:#00F2FE; margin-top:8px;">DataCleaner AI</div>
        <div style="font-size:0.7rem; color:#64748B; letter-spacing:2px; text-transform:uppercase; margin-top:4px;">
            Enterprise v3.0
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    if st.session_state['raw_df'] is not None:
        df_s = st.session_state['raw_df']
        miss_s = int(df_s.isnull().sum().sum())
        dups_s = int(df_s.duplicated().sum())
        health_s = round(max(0, 100 - (miss_s/max(df_s.size,1)*100) - (dups_s/max(len(df_s),1)*100)), 1)
        h_col = '#22C55E' if health_s > 75 else ('#F59E0B' if health_s > 40 else '#EF4444')
        st.markdown(
            f'<div style="background:rgba(0,242,254,0.05); border:1px solid rgba(0,242,254,0.15);'
            f'border-radius:12px; padding:14px; font-size:0.82rem; color:#94A3B8; line-height:2.1;">'
            f'<div style="font-weight:700; color:#E2E8F0; margin-bottom:8px;">📋 Active Dataset</div>'
            f'📐 Rows: <b style="color:#00F2FE">{df_s.shape[0]:,}</b><br>'
            f'📏 Cols: <b style="color:#00F2FE">{df_s.shape[1]}</b><br>'
            f'❓ Missing: <b style="color:#F59E0B">{miss_s:,}</b><br>'
            f'🧬 Health: <b style="color:{h_col}">{health_s}/100</b>'
            f'</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div style="background:rgba(255,255,255,0.02); border:1px dashed rgba(255,255,255,0.1);'
            'border-radius:10px; padding:14px; font-size:0.82rem; color:#64748B; text-align:center;">'
            '📂 No dataset loaded.<br>Go to <b style="color:#00F2FE">Dashboard</b> to upload.'
            '</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        '<div style="color:#475569; font-size:0.7rem; text-align:center; line-height:1.9;">'
        'Streamlit · Plotly · scikit-learn · pandas<br>'
        '<span style="color:#00F2FE;">DataCleaner AI © 2024</span>'
        '</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  HERO
# ═══════════════════════════════════════════════
st.markdown("""
<div style="text-align:center; padding:56px 0 28px 0;" class="fade-up">
    <div style="display:inline-flex; align-items:center; gap:8px;
        background:rgba(0,242,254,0.07); border:1px solid rgba(0,242,254,0.3);
        border-radius:50px; padding:8px 22px; font-size:0.76rem; color:#00F2FE;
        letter-spacing:2px; text-transform:uppercase; margin-bottom:28px;">
        <span style="width:7px;height:7px;background:#00F2FE;border-radius:50%;
            display:inline-block; box-shadow:0 0 8px #00F2FE;"></span>
        Enterprise Edition &nbsp;·&nbsp; Production Ready
    </div>
    <div style="font-size:4.6rem; font-weight:900; color:#FFFFFF;
        letter-spacing:-3px; line-height:1.0; margin-bottom:14px;">
        DataCleaner <span style="color:#00F2FE;">AI</span>
    </div>
    <div style="font-size:1.35rem; font-weight:300; color:#4FACFE;
        letter-spacing:1px; margin-bottom:20px;">
        From Raw Chaos &nbsp;→&nbsp; Clean Intelligence
    </div>
    <p style="color:#94A3B8; font-size:1.05rem; max-width:660px; margin:0 auto;
        line-height:1.9; font-weight:400;">
        Upload any messy dataset and let AI automatically detect quality issues,
        clean, transform, visualize, and generate a production-ready Python pipeline —
        <b style="color:#CBD5E1;">no coding required.</b>
    </p>
</div>
""", unsafe_allow_html=True)

# ── Stat strip ──
st.markdown("""
<div style="display:flex; justify-content:center; gap:0;
    border:1px solid rgba(255,255,255,0.07); border-radius:16px;
    background:rgba(255,255,255,0.01); overflow:hidden; margin:0 auto 40px auto; max-width:700px;">
    <div style="flex:1; text-align:center; padding:20px 16px; border-right:1px solid rgba(255,255,255,0.06);">
        <div style="font-size:1.9rem; font-weight:800; color:#00F2FE;">8</div>
        <div style="color:#64748B; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; margin-top:2px;">Modules</div>
    </div>
    <div style="flex:1; text-align:center; padding:20px 16px; border-right:1px solid rgba(255,255,255,0.06);">
        <div style="font-size:1.9rem; font-weight:800; color:#4FACFE;">20+</div>
        <div style="color:#64748B; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; margin-top:2px;">Cleaning Ops</div>
    </div>
    <div style="flex:1; text-align:center; padding:20px 16px; border-right:1px solid rgba(255,255,255,0.06);">
        <div style="font-size:1.9rem; font-weight:800; color:#00F2FE;">7</div>
        <div style="color:#64748B; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; margin-top:2px;">Chart Types</div>
    </div>
    <div style="flex:1; text-align:center; padding:20px 16px; border-right:1px solid rgba(255,255,255,0.06);">
        <div style="font-size:1.9rem; font-weight:800; color:#4FACFE;">ML</div>
        <div style="color:#64748B; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; margin-top:2px;">Powered</div>
    </div>
    <div style="flex:1; text-align:center; padding:20px 16px;">
        <div style="font-size:1.9rem; font-weight:800; color:#00F2FE;">100%</div>
        <div style="color:#64748B; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; margin-top:2px;">No-Code</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  FEATURES GRID
# ═══════════════════════════════════════════════
st.markdown("""
<div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
    <div style="width:4px;height:28px;background:linear-gradient(180deg,#4FACFE,#00F2FE);border-radius:4px;"></div>
    <span style="font-size:1.25rem; font-weight:700; color:#E2E8F0;">✦ Core Modules</span>
</div>
""", unsafe_allow_html=True)

features = [
    ("🏠", "Dashboard",        "#00F2FE", "Upload CSV/Excel, live health score, column profiling & AI insights"),
    ("🔍", "Data Overview",    "#4FACFE", "Full quality report — types, distributions, skewness, unique counts"),
    ("🧹", "Smart Cleaning",   "#22C55E", "KNN/Mean/Median imputation, outlier capping, text & date cleaning"),
    ("🛡️", "Data Privacy",     "#A78BFA", "Auto-detect PII — hash, mask or drop emails, phones, names"),
    ("⚙️", "Transformations",  "#34D399", "Min-Max/Standard scaling, One-Hot/Label encoding, feature engineering"),
    ("📊", "Visualizations",   "#F59E0B", "7 interactive Plotly charts — Raw vs Cleaned always side-by-side"),
    ("💻", "Code Generator",   "#00F2FE", "Auto-generate a reproducible Python cleaning pipeline script"),
    ("🆚", "Compare & Export", "#4FACFE", "Before/after diff with delta stats — export as CSV or Excel"),
]

cols = st.columns(4)
for i, (icon, title, color, desc) in enumerate(features):
    with cols[i % 4]:
        st.markdown(
            f'<div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.07);'
            f'border-radius:16px; padding:22px 18px; margin-bottom:16px; text-align:center;'
            f'transition:all 0.3s ease; cursor:default;"'
            f'onmouseover="this.style.borderColor=\'{color}66\';this.style.transform=\'translateY(-5px)\';this.style.boxShadow=\'0 12px 32px {color}18\'"'
            f'onmouseout="this.style.borderColor=\'rgba(255,255,255,0.07)\';this.style.transform=\'translateY(0)\';this.style.boxShadow=\'none\'">'
            f'<div style="font-size:2.2rem; margin-bottom:12px;">{icon}</div>'
            f'<div style="width:32px;height:3px;background:{color};border-radius:2px;margin:0 auto 10px;"></div>'
            f'<div style="font-weight:700; color:#E2E8F0; font-size:0.9rem; margin-bottom:7px;">{title}</div>'
            f'<div style="color:#64748B; font-size:0.74rem; line-height:1.65;">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True)
    if i == 3:
        cols = st.columns(4)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  HOW IT WORKS
# ═══════════════════════════════════════════════
st.markdown("""
<div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
    <div style="width:4px;height:28px;background:linear-gradient(180deg,#4FACFE,#00F2FE);border-radius:4px;"></div>
    <span style="font-size:1.25rem; font-weight:700; color:#E2E8F0;">⚡ How It Works</span>
</div>
""", unsafe_allow_html=True)

steps = [
    ("01", "Upload",    "📂", "#00F2FE", "Drop any CSV or Excel — auto-detects types and calculates quality instantly."),
    ("02", "Analyse",   "🔍", "#4FACFE", "Full health report: missing values, duplicates, skewness, PII detection."),
    ("03", "Clean",     "🧹", "#22C55E", "ML-powered: KNN imputation, outlier capping, text & date normalization."),
    ("04", "Transform", "⚙️", "#34D399", "Scale features, encode categories, engineer new columns with one click."),
    ("05", "Visualize", "📊", "#F59E0B", "7 charts comparing raw vs cleaned — confirm every change visually."),
    ("06", "Export",    "🚀", "#A78BFA", "Download cleaned data as CSV/Excel + auto-generated Python script."),
]

step_cols = st.columns(6)
for col, (num, title, icon, color, desc) in zip(step_cols, steps):
    with col:
        st.markdown(
            f'<div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06);'
            f'border-radius:14px; padding:20px 12px; text-align:center; height:100%;">'
            f'<div style="font-size:0.65rem; color:{color}; font-weight:800; letter-spacing:3px; margin-bottom:10px;">STEP {num}</div>'
            f'<div style="font-size:2rem; margin-bottom:10px;">{icon}</div>'
            f'<div style="font-weight:700; color:#E2E8F0; font-size:0.85rem; margin-bottom:8px;">{title}</div>'
            f'<div style="color:#64748B; font-size:0.71rem; line-height:1.7;">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  TECH STACK
# ═══════════════════════════════════════════════
st.markdown("""
<hr style="border-color:rgba(255,255,255,0.06); margin:10px 0 28px 0;">
<div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
    <div style="width:4px;height:28px;background:linear-gradient(180deg,#4FACFE,#00F2FE);border-radius:4px;"></div>
    <span style="font-size:1.25rem; font-weight:700; color:#E2E8F0;">🛠️ Tech Stack</span>
</div>
""", unsafe_allow_html=True)

tech = [
    ("🐍", "Python 3.9+",    "Core language"),
    ("⚡", "Streamlit",      "UI framework"),
    ("📊", "Plotly",         "Interactive charts"),
    ("🧠", "scikit-learn",   "KNN Imputation"),
    ("📐", "pandas",         "Data manipulation"),
    ("🔢", "NumPy",          "Numerical ops"),
    ("📈", "SciPy",          "KDE & stats"),
    ("📁", "openpyxl",       "Excel export"),
]

tc = st.columns(8)
for col, (icon, name, role) in zip(tc, tech):
    with col:
        st.markdown(
            f'<div style="text-align:center; padding:16px 8px; background:rgba(255,255,255,0.02);'
            f'border:1px solid rgba(255,255,255,0.06); border-radius:12px;">'
            f'<div style="font-size:1.6rem; margin-bottom:6px;">{icon}</div>'
            f'<div style="font-weight:700; color:#E2E8F0; font-size:0.78rem;">{name}</div>'
            f'<div style="color:#475569; font-size:0.68rem; margin-top:2px;">{role}</div>'
            f'</div>',
            unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  CTA
# ═══════════════════════════════════════════════
st.markdown("""
<br>
<hr style="border-color:rgba(255,255,255,0.06);">
<div style="text-align:center; padding:40px 20px;">
    <div style="font-size:1.5rem; font-weight:800; color:#FFFFFF; margin-bottom:10px;">
        Ready to clean your data? 🚀
    </div>
    <div style="color:#64748B; font-size:0.9rem; margin-bottom:24px;">
        Navigate to <b style="color:#00F2FE;">Dashboard</b> in the sidebar to upload your dataset and get started.
    </div>
</div>
""", unsafe_allow_html=True)
