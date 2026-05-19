import streamlit as st
import warnings
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Dashboard | DataCleaner AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

from modules.ui import PREMIUM_CSS, SIDEBAR_HTML

st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

# ── Session state ──
for key, default in [('raw_df', None), ('cleaned_df', None), ('cleaning_logs', [])]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Sidebar ──
with st.sidebar:
    st.markdown(SIDEBAR_HTML, unsafe_allow_html=True)
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
            f'🗂️ Dupes: <b style="color:#F59E0B">{dups_s:,}</b><br>'
            f'🧬 Health: <b style="color:{h_col}">{health_s}/100</b>'
            f'</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div style="background:rgba(255,255,255,0.02); border:1px dashed rgba(255,255,255,0.1);'
            'border-radius:10px; padding:14px; font-size:0.82rem; color:#64748B; text-align:center;">'
            '📂 Upload a dataset below to begin.'
            '</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  PAGE HEADER
# ═══════════════════════════════════════════════
st.markdown("""
<div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
    <div style="width:4px;height:32px;background:linear-gradient(180deg,#4FACFE,#00F2FE);border-radius:4px;"></div>
    <span style="font-size:1.6rem; font-weight:800; color:#E2E8F0;">📊 Dashboard</span>
</div>
<p style="color:#64748B; font-size:0.88rem; margin:0 0 24px 14px;">
    Upload your dataset — the dashboard auto-profiles it and gives you a full quality report.
</p>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  UPLOAD SECTION
# ═══════════════════════════════════════════════
up_col, tip_col = st.columns([3, 2])

with up_col:
    from modules.upload import show_upload_module
    from modules.memory import optimize_memory
    df = show_upload_module()

with tip_col:
    st.markdown("""
    <div style="background:rgba(0,242,254,0.04); border:1px solid rgba(0,242,254,0.15);
        border-radius:16px; padding:22px 24px;">
        <div style="font-weight:700; color:#E2E8F0; margin-bottom:14px; font-size:0.92rem;">
            💡 Supported Formats & Tips
        </div>
        <div style="color:#94A3B8; font-size:0.82rem; line-height:2.3;">
            ✅ &nbsp;<b style="color:#E2E8F0;">CSV</b> — comma or semicolon delimited<br>
            ✅ &nbsp;<b style="color:#E2E8F0;">Excel</b> — .xlsx and .xls files<br>
            ✅ &nbsp;<b style="color:#E2E8F0;">Any size</b> — memory auto-optimized on load<br>
            ✅ &nbsp;<b style="color:#E2E8F0;">Mixed types</b> — numeric, text, dates, PII<br>
            ✅ &nbsp;<b style="color:#E2E8F0;">Messy data</b> — missing, dupes, outliers OK<br>
        </div>
        <div style="margin-top:14px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.06);
            color:#475569; font-size:0.75rem;">
            🧪 No dataset? Use <b style="color:#00F2FE;">test_dataset.csv</b> included in the project root.
        </div>
    </div>
    """, unsafe_allow_html=True)

if df is not None:
    with st.spinner("⚡ Optimizing memory footprint..."):
        opt_df, init_mem, final_mem = optimize_memory(df)
    st.session_state['raw_df']        = opt_df
    st.session_state['cleaned_df']    = opt_df.copy()
    st.session_state['cleaning_logs'] = []
    st.success(f"✅ Dataset loaded! Memory optimised: {init_mem:.1f} MB → {final_mem:.1f} MB")

# ═══════════════════════════════════════════════
#  DASHBOARD (after upload)
# ═══════════════════════════════════════════════
if st.session_state['raw_df'] is not None:
    df = st.session_state['raw_df']

    total_cells  = df.shape[0] * df.shape[1]
    missing      = int(df.isnull().sum().sum())
    missing_pct  = round(missing / max(total_cells, 1) * 100, 2)
    dups         = int(df.duplicated().sum())
    num_cols     = df.select_dtypes(include='number').columns.tolist()
    cat_cols     = df.select_dtypes(include=['object', 'category']).columns.tolist()
    health_score = round(max(0, 100 - missing_pct - (dups / max(len(df), 1) * 100)), 1)
    h_color      = '#22C55E' if health_score > 75 else ('#F59E0B' if health_score > 40 else '#EF4444')
    h_label      = '🟢 Healthy' if health_score > 75 else ('🟡 Needs Attention' if health_score > 40 else '🔴 Critical')

    st.markdown("<hr style='border-color:rgba(255,255,255,0.06); margin:28px 0 22px 0;'>", unsafe_allow_html=True)

    # ── Section header ──
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
        <div style="width:4px;height:28px;background:linear-gradient(180deg,#4FACFE,#00F2FE);border-radius:4px;"></div>
        <span style="font-size:1.25rem; font-weight:700; color:#E2E8F0;">🧬 Dataset Health Report</span>
    </div>
    """, unsafe_allow_html=True)

    # ── 6 metrics ──
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Total Rows",      f"{df.shape[0]:,}")
    m2.metric("Columns",         df.shape[1])
    m3.metric("Missing Values",  f"{missing:,}", f"{missing_pct}%")
    m4.metric("Duplicates",      f"{dups:,}")
    m5.metric("Numeric Cols",    len(num_cols))
    m6.metric("Text Cols",       len(cat_cols))

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Health Score Bar ──
    st.markdown(
        f'<div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.07);'
        f'border-radius:16px; padding:22px 28px; margin-bottom:22px;">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">'
        f'<span style="color:#E2E8F0; font-weight:700; font-size:1rem;">Overall Health Score</span>'
        f'<span style="font-size:0.95rem; color:{h_color}; font-weight:800;">{h_label} &nbsp;·&nbsp; {health_score} / 100</span>'
        f'</div>'
        f'<div style="background:rgba(255,255,255,0.06); border-radius:50px; height:12px; overflow:hidden;">'
        f'<div style="width:{health_score}%; height:100%; border-radius:50px;'
        f'background:linear-gradient(90deg,{h_color},{h_color}cc);'
        f'box-shadow:0 0 16px {h_color}66;"></div>'
        f'</div>'
        f'<div style="display:flex; justify-content:space-between; margin-top:8px;'
        f'font-size:0.72rem; color:#475569;">'
        f'<span>0 — Critical</span><span>50 — Fair</span><span>100 — Perfect</span>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True)

    # ── Issue Breakdown Cards ──
    ic1, ic2, ic3, ic4 = st.columns(4)
    issues = [
        (ic1, "Missing Cells",    missing,      f"{missing_pct}% of all data",          '#F59E0B'),
        (ic2, "Duplicate Rows",   dups,         f"{round(dups/max(len(df),1)*100,1)}% of rows", '#EF4444'),
        (ic3, "Numeric Columns",  len(num_cols), "ready for scaling / ML",              '#00F2FE'),
        (ic4, "Text Columns",     len(cat_cols), "ready for encoding / NLP",            '#4FACFE'),
    ]
    for col, label, val, sub, color in issues:
        with col:
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.02); border:1px solid {color}22;'
                f'border-radius:14px; padding:18px; text-align:center; margin-bottom:4px;">'
                f'<div style="font-size:2.1rem; font-weight:800; color:{color};">{val:,}</div>'
                f'<div style="color:#E2E8F0; font-weight:600; font-size:0.84rem; margin:5px 0;">{label}</div>'
                f'<div style="color:#64748B; font-size:0.72rem;">{sub}</div>'
                f'</div>',
                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 5 Analysis Tabs ──
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📄 Data Preview",
        "📊 Column Statistics",
        "❓ Missing Values Map",
        "📈 Distribution Explorer",
        "🏷️ Category Breakdown"
    ])

    with tab1:
        rows_to_show = st.slider("Rows to preview", 5, min(200, len(df)), 15, key="preview_slider")
        st.dataframe(df.head(rows_to_show), use_container_width=True)
        type_counts = df.dtypes.astype(str).value_counts()
        tc_html = ' &nbsp;|&nbsp; '.join(
            f'<span style="color:#00F2FE;">{v}</span> <span style="color:#64748B;">{k}</span>'
            for k, v in type_counts.items()
        )
        st.markdown(
            f'<div style="font-size:0.78rem; color:#64748B; margin-top:6px;">'
            f'Showing {rows_to_show} of {len(df):,} rows &nbsp;·&nbsp; Column types: {tc_html}'
            f'</div>', unsafe_allow_html=True)

    with tab2:
        if num_cols:
            st.markdown("<div style='color:#64748B; font-size:0.82rem; margin-bottom:8px;'>Numeric column statistics (with skewness & kurtosis)</div>", unsafe_allow_html=True)
            stats_df = df[num_cols].describe().T.round(3)
            stats_df['skewness'] = df[num_cols].skew().round(3)
            stats_df['kurtosis'] = df[num_cols].kurt().round(3)
            st.dataframe(stats_df, use_container_width=True)
        else:
            st.info("No numeric columns found.")
        if cat_cols:
            st.markdown("<br><div style='color:#64748B; font-size:0.82rem; margin-bottom:8px;'>Categorical column summary</div>", unsafe_allow_html=True)
            cat_stats = pd.DataFrame({
                'Column':   cat_cols,
                'Unique':   [df[c].nunique() for c in cat_cols],
                'Missing':  [int(df[c].isnull().sum()) for c in cat_cols],
                'Top Value':[str(df[c].mode()[0]) if not df[c].mode().empty else 'N/A' for c in cat_cols],
                'Freq':     [int(df[c].value_counts().iloc[0]) if len(df[c].value_counts())>0 else 0 for c in cat_cols],
            })
            st.dataframe(cat_stats, use_container_width=True, hide_index=True)

    with tab3:
        miss_series = df.isnull().sum().sort_values(ascending=False)
        miss_series = miss_series[miss_series > 0]
        if len(miss_series) == 0:
            st.success("✅ No missing values — this dataset is 100% complete!")
        else:
            pct_series = (miss_series / len(df) * 100).round(1)
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=miss_series.values, y=miss_series.index, orientation='h',
                marker=dict(color=pct_series.values, colorscale='Blues',
                            showscale=True, colorbar=dict(title='%')),
                text=[f"{v:,} ({p}%)" for v, p in zip(miss_series.values, pct_series.values)],
                textposition='auto'
            ))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E2E8F0', family='Outfit'),
                title='Missing Values per Column',
                height=max(300, len(miss_series)*42),
                xaxis=dict(gridcolor='rgba(255,255,255,0.06)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.06)'),
                margin=dict(t=50, b=40, l=20, r=20)
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab4:
        if num_cols:
            sel_col = st.selectbox("Select numeric column", num_cols, key="dist_dash")
            data = df[sel_col].dropna().astype(float)
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=data, nbinsx=50, marker_color='#00F2FE', opacity=0.7, name=sel_col))
            try:
                from scipy import stats as sp
                x_r = np.linspace(float(data.min()), float(data.max()), 300)
                kde = sp.gaussian_kde(data)
                bw  = (data.max()-data.min())/50 if data.max()!=data.min() else 1
                fig.add_trace(go.Scatter(x=x_r, y=kde(x_r)*len(data)*bw,
                                         name='KDE', line=dict(color='#4FACFE', width=2.5, dash='dot')))
            except Exception:
                pass
            skew_val  = round(float(df[sel_col].skew()), 3)
            skew_note = "right-skewed" if skew_val > 1 else ("left-skewed" if skew_val < -1 else "approx. normal")
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E2E8F0', family='Outfit'),
                title=f"Distribution: {sel_col}  (Skewness: {skew_val} — {skew_note})",
                height=380, xaxis=dict(gridcolor='rgba(255,255,255,0.06)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.06)'),
                margin=dict(t=50, b=40, l=20, r=20)
            )
            st.plotly_chart(fig, use_container_width=True)

            # Skewness summary for all columns
            skew_df = pd.DataFrame({
                'Column':   num_cols,
                'Skewness': [round(float(df[c].skew()), 3) for c in num_cols],
                'Kurtosis': [round(float(df[c].kurt()), 3) for c in num_cols],
            }).sort_values('Skewness', key=abs, ascending=False)
            skew_df['Status'] = skew_df['Skewness'].apply(
                lambda x: '⚠️ Highly Skewed' if abs(x)>1 else ('🟡 Mild' if abs(x)>0.5 else '✅ Normal'))
            st.dataframe(skew_df.reset_index(drop=True), use_container_width=True, hide_index=True)
        else:
            st.info("No numeric columns to plot.")

    with tab5:
        if cat_cols:
            sel_cat = st.selectbox("Select text column", cat_cols, key="cat_dash")
            top_n   = st.slider("Top N values", 5, 30, 15, key="cat_dash_n")
            vc = df[sel_cat].value_counts().head(top_n)
            vc_df = pd.DataFrame({'Category': vc.index.astype(str), 'Count': vc.values})
            vc_df['Percentage'] = (vc_df['Count'] / vc_df['Count'].sum() * 100).round(1)

            c_chart, c_table = st.columns([2, 1])
            with c_chart:
                fig = px.bar(vc_df, x='Category', y='Count', color='Count',
                             color_continuous_scale='Blues', title=f"Top {top_n} — {sel_cat}")
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#E2E8F0', family='Outfit'), height=340,
                    xaxis=dict(gridcolor='rgba(255,255,255,0.06)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.06)'),
                    margin=dict(t=50, b=60, l=20, r=20)
                )
                st.plotly_chart(fig, use_container_width=True)
            with c_table:
                st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
                st.dataframe(vc_df, use_container_width=True, hide_index=True)
        else:
            st.info("No text/categorical columns found.")

    # ── CTA row ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align:center; color:#64748B; font-size:0.85rem; margin-bottom:12px;">'
        '🚀 Dataset ready! Use the sidebar to navigate to the next step.'
        '</div>', unsafe_allow_html=True)
    b1, b2, b3, b4 = st.columns(4)
    with b1: st.button("🔍 Data Overview →",    use_container_width=True)
    with b2: st.button("🧹 Smart Cleaning →",    use_container_width=True)
    with b3: st.button("📊 Visualizations →",    use_container_width=True)
    with b4: st.button("🆚 Compare & Export →", use_container_width=True)

else:
    # Empty state
    st.markdown("""
    <div style="text-align:center; padding:60px 20px; background:rgba(255,255,255,0.01);
        border:1px dashed rgba(0,242,254,0.15); border-radius:20px; margin-top:20px;">
        <div style="font-size:4rem; margin-bottom:16px;">📂</div>
        <div style="font-size:1.15rem; font-weight:700; color:#E2E8F0; margin-bottom:8px;">
            Upload a dataset above to unlock the full dashboard
        </div>
        <div style="color:#64748B; font-size:0.88rem; line-height:1.8;">
            Supports CSV and Excel &nbsp;·&nbsp; Auto memory optimization
            &nbsp;·&nbsp; Works with any messy data
        </div>
    </div>
    """, unsafe_allow_html=True)
