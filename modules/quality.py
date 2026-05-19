import streamlit as st
import pandas as pd
import plotly.express as px
from modules.ui import PREMIUM_CSS, SIDEBAR_HTML, section_header
from utils.ai_suggestions import get_data_quality_score
from utils.insights import generate_dataset_insights

def show_quality_analysis(df):
    st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

    if df is None:
        st.info("Please upload a dataset on the Home page first.")
        return

    score = get_data_quality_score(df)
    color = "#22C55E" if score > 75 else ("#F59E0B" if score > 40 else "#EF4444")
    label = "Excellent" if score > 75 else ("Needs Attention" if score > 40 else "Critically Dirty")

    section_header("🔍", "Data Quality Analysis", "A deep-dive into the structural health of your dataset.")

    # ── Quality Score Banner ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(79,172,254,0.08),rgba(0,242,254,0.04));
        border:1px solid rgba(0,242,254,0.2); border-radius:18px; padding:24px 30px; margin-bottom:24px;">
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px;">
            <div>
                <div style="font-size:0.78rem; color:#64748B; text-transform:uppercase; letter-spacing:2px; margin-bottom:6px;">
                    Overall Quality Score
                </div>
                <div style="font-size:3.5rem; font-weight:900; color:{color}; line-height:1;">
                    {score}<span style="font-size:1.5rem; color:#64748B;">/100</span>
                </div>
                <div style="color:{color}; font-weight:600; font-size:1rem; margin-top:6px;">● {label}</div>
            </div>
            <div style="flex:1; min-width:200px;">
                <div style="background:rgba(255,255,255,0.06); border-radius:50px; height:14px; overflow:hidden;">
                    <div style="width:{score}%; height:100%; border-radius:50px;
                        background:linear-gradient(90deg,{color},{color}cc);
                        box-shadow:0 0 16px {color}88;"></div>
                </div>
                <div style="color:#64748B; font-size:0.78rem; margin-top:10px; line-height:1.7;">
                    Score is calculated from missing value density, duplicate ratio, and type consistency.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Key metrics row ──
    total_cells = df.shape[0] * df.shape[1]
    missing = df.isnull().sum().sum()
    dups = df.duplicated().sum()
    num_cols_count = len(df.select_dtypes(include='number').columns)
    cat_cols_count = len(df.select_dtypes(include=['object','category']).columns)

    m1,m2,m3,m4,m5 = st.columns(5)
    m1.metric("Total Rows",     f"{df.shape[0]:,}")
    m2.metric("Total Columns",  df.shape[1])
    m3.metric("Missing Cells",  f"{missing:,}", f"{missing/total_cells*100:.1f}%")
    m4.metric("Duplicates",     f"{dups:,}")
    m5.metric("Numeric / Text", f"{num_cols_count} / {cat_cols_count}")

    # ── AI Insights ──
    st.markdown("<br>", unsafe_allow_html=True)
    section_header("🧠", "AI-Powered Insights")
    insights = generate_dataset_insights(df)
    cols = st.columns(2)
    for i, insight in enumerate(insights):
        cols[i % 2].markdown(f"""
        <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(0,242,254,0.1);
            border-radius:12px; padding:14px 18px; margin-bottom:10px; color:#CBD5E1; font-size:0.88rem; line-height:1.6;">
            {insight}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["❓ Missing Values", "🗂️ Duplicates & Types", "📈 Statistics", "📊 Distribution Charts"])

    with tab1:
        missing_data = pd.DataFrame({
            'Column': df.columns,
            'Missing Values': df.isnull().sum().values,
            '% Missing': (df.isnull().sum().values / len(df) * 100).round(2),
            'Data Type': df.dtypes.astype(str).values
        }).sort_values('Missing Values', ascending=False)
        missing_only = missing_data[missing_data['Missing Values'] > 0]

        if len(missing_only) == 0:
            st.markdown("""
            <div style="text-align:center; padding:40px; background:rgba(34,197,94,0.06);
                border:1px solid rgba(34,197,94,0.2); border-radius:16px;">
                <div style="font-size:2.5rem; margin-bottom:12px;">✅</div>
                <div style="color:#22C55E; font-weight:700; font-size:1.1rem;">No missing values found!</div>
                <div style="color:#64748B; font-size:0.85rem; margin-top:6px;">Your dataset is complete.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.dataframe(missing_only.style.background_gradient(subset=['% Missing'], cmap='Reds'),
                         use_container_width=True)
            fig = px.bar(missing_only, x='Column', y='Missing Values', color='% Missing',
                         color_continuous_scale='Reds', title="Missing Values per Column")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            section_header("🗂️", "Duplicate Rows")
            dups_count = df.duplicated().sum()
            st.metric("Duplicate Rows Found", f"{dups_count:,}")
            if dups_count > 0:
                st.warning(f"⚠️ {dups_count} duplicate rows detected. Go to Smart Cleaning to remove them.")
                st.dataframe(df[df.duplicated(keep=False)].head(10), use_container_width=True)
            else:
                st.success("✅ No duplicates found!")
        with c2:
            section_header("🏷️", "Data Types per Column")
            dtype_df = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.astype(str).values,
                'Unique Values': [df[c].nunique() for c in df.columns],
                'Sample': [str(df[c].dropna().iloc[0]) if len(df[c].dropna()) > 0 else 'N/A' for c in df.columns]
            })
            st.dataframe(dtype_df, use_container_width=True)

    with tab3:
        st.dataframe(df.describe(include='all').T.style.background_gradient(cmap='Blues'),
                     use_container_width=True)

    with tab4:
        num_cols = df.select_dtypes(include='number').columns.tolist()
        if num_cols:
            selected = st.selectbox("Select column to visualize", num_cols, key="quality_dist_col")
            fig = px.histogram(df, x=selected, nbins=40, color_discrete_sequence=['#00F2FE'],
                               title=f"Distribution of {selected}")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns available for charting.")
