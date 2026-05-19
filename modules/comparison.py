import streamlit as st
import pandas as pd
import io
import plotly.express as px
from modules.ui import PREMIUM_CSS, section_header

def show_comparison_and_export(raw_df, cleaned_df, logs):
    st.markdown(PREMIUM_CSS, unsafe_allow_html=True)
    section_header("🆚", "Compare & Export",
                   "Side-by-side comparison of raw vs cleaned dataset, plus multi-format export.")

    if raw_df is None or cleaned_df is None:
        st.info("Please upload a dataset on the Home page first.")
        return

    initial_rows   = len(raw_df)
    final_rows     = len(cleaned_df)
    initial_miss   = raw_df.isnull().sum().sum()
    final_miss     = cleaned_df.isnull().sum().sum()
    initial_dups   = raw_df.duplicated().sum()
    final_dups     = cleaned_df.duplicated().sum()
    col_delta      = len(cleaned_df.columns) - len(raw_df.columns)

    # ── Summary Banner ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(79,172,254,0.08),rgba(0,242,254,0.04));
        border:1px solid rgba(0,242,254,0.2); border-radius:18px; padding:22px 28px; margin-bottom:22px;">
        <div style="font-weight:700; color:#E2E8F0; font-size:1.05rem; margin-bottom:16px;">
            📊 Cleaning Summary
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:12px;">
            <div style="flex:1; min-width:130px; background:rgba(0,0,0,0.2); border-radius:12px; padding:14px; text-align:center;">
                <div style="font-size:1.5rem; font-weight:800; color:#00F2FE;">{final_rows:,}</div>
                <div style="color:#64748B; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px;">Final Rows</div>
                <div style="color:#F87171; font-size:0.78rem; margin-top:4px;">{'-' if initial_rows - final_rows > 0 else ''}{initial_rows - final_rows:,} removed</div>
            </div>
            <div style="flex:1; min-width:130px; background:rgba(0,0,0,0.2); border-radius:12px; padding:14px; text-align:center;">
                <div style="font-size:1.5rem; font-weight:800; color:#4FACFE;">{final_miss:,}</div>
                <div style="color:#64748B; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px;">Missing Left</div>
                <div style="color:#22C55E; font-size:0.78rem; margin-top:4px;">-{initial_miss - final_miss:,} resolved</div>
            </div>
            <div style="flex:1; min-width:130px; background:rgba(0,0,0,0.2); border-radius:12px; padding:14px; text-align:center;">
                <div style="font-size:1.5rem; font-weight:800; color:#22C55E;">{final_dups:,}</div>
                <div style="color:#64748B; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px;">Duplicates Left</div>
                <div style="color:#22C55E; font-size:0.78rem; margin-top:4px;">-{initial_dups - final_dups:,} removed</div>
            </div>
            <div style="flex:1; min-width:130px; background:rgba(0,0,0,0.2); border-radius:12px; padding:14px; text-align:center;">
                <div style="font-size:1.5rem; font-weight:800; color:#A78BFA;">{len(cleaned_df.columns)}</div>
                <div style="color:#64748B; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px;">Final Columns</div>
                <div style="color:{'#22C55E' if col_delta >= 0 else '#F87171'}; font-size:0.78rem; margin-top:4px;">{'+' if col_delta >= 0 else ''}{col_delta} vs raw</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Before / After chart ──
    before_after = pd.DataFrame({
        'Metric': ['Missing Values', 'Duplicate Rows'],
        'Before': [initial_miss, initial_dups],
        'After': [final_miss, final_dups]
    })
    fig = px.bar(before_after, x='Metric', y=['Before', 'After'],
                 barmode='group', color_discrete_sequence=['#EF4444', '#22C55E'],
                 title="Before vs After Cleaning")
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
    st.plotly_chart(fig, use_container_width=True)

    # ── Side-by-side preview ──
    st.markdown("<br>", unsafe_allow_html=True)
    section_header("👁️", "Side-by-Side Preview")
    col_raw, col_clean = st.columns(2)
    with col_raw:
        st.markdown("<span style='color:#F87171; font-weight:700;'>🔴 Raw Dataset</span>", unsafe_allow_html=True)
        st.dataframe(raw_df.head(8), use_container_width=True)
    with col_clean:
        st.markdown("<span style='color:#22C55E; font-weight:700;'>🟢 Cleaned Dataset</span>", unsafe_allow_html=True)
        st.dataframe(cleaned_df.head(8), use_container_width=True)

    # ── Export ──
    st.markdown("<br>", unsafe_allow_html=True)
    section_header("📥", "Export Your Data")
    d1, d2, d3 = st.columns(3)

    with d1:
        csv_data = cleaned_df.to_csv(index=False).encode('utf-8')
        st.markdown("""
        <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(0,242,254,0.15);
            border-radius:14px; padding:18px; text-align:center; margin-bottom:8px;">
            <div style="font-size:2rem;">📄</div>
            <div style="font-weight:700; color:#E2E8F0; margin:6px 0 4px;">CSV Format</div>
            <div style="color:#64748B; font-size:0.78rem;">Universal, works everywhere</div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button("⬇️ Download CSV", csv_data, "cleaned_dataset.csv", "text/csv",
                           use_container_width=True, type="primary")

    with d2:
        try:
            parquet_buf = io.BytesIO()
            cleaned_df.to_parquet(parquet_buf, index=False, engine='fastparquet')
            st.markdown("""
            <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(167,139,250,0.25);
                border-radius:14px; padding:18px; text-align:center; margin-bottom:8px;">
                <div style="font-size:2rem;">⚡</div>
                <div style="font-weight:700; color:#E2E8F0; margin:6px 0 4px;">Parquet Format</div>
                <div style="color:#64748B; font-size:0.78rem;">Big Data standard, 10× faster</div>
            </div>
            """, unsafe_allow_html=True)
            st.download_button("⬇️ Download Parquet", parquet_buf.getvalue(), "cleaned_dataset.parquet",
                               "application/octet-stream", use_container_width=True, type="primary")
        except Exception as e:
            st.error(f"Parquet error: {e}")

    with d3:
        report = f"DataCleaner AI — Cleaning Report\n{'='*40}\n\n"
        report += f"Initial: {initial_rows} rows, {initial_miss} missing, {initial_dups} duplicates\n"
        report += f"Final:   {final_rows} rows, {final_miss} missing, {final_dups} duplicates\n\n"
        report += "Applied Steps:\n" + ("\n".join([f"  • {l}" for l in logs]) if logs else "  None")
        st.markdown("""
        <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(34,197,94,0.2);
            border-radius:14px; padding:18px; text-align:center; margin-bottom:8px;">
            <div style="font-size:2rem;">📋</div>
            <div style="font-weight:700; color:#E2E8F0; margin:6px 0 4px;">Cleaning Report</div>
            <div style="color:#64748B; font-size:0.78rem;">Text summary of all steps</div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button("⬇️ Download Report", report, "cleaning_report.txt", "text/plain",
                           use_container_width=True)

    # ── Cleaning log ──
    if logs:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(0,242,254,0.12);
            border-radius:12px; padding:14px 20px; margin-bottom:6px;">
            <div style="font-weight:700; color:#E2E8F0; font-size:0.9rem;">📋 Full Cleaning Log</div>
        </div>
        """, unsafe_allow_html=True)
        for log in logs:
            st.markdown(f"<div style='color:#94A3B8; font-size:0.85rem; padding:3px 4px;'>✅ {log}</div>",
                        unsafe_allow_html=True)
