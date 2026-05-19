import streamlit as st
import pandas as pd
import hashlib
from modules.ui import PREMIUM_CSS, section_header

def show_privacy_options(df):
    st.markdown(PREMIUM_CSS, unsafe_allow_html=True)
    section_header("🛡️", "Data Privacy & Anonymization",
                   "Detect and mask Personally Identifiable Information (PII) before exporting your data.")

    if df is None:
        st.info("Please upload a dataset on the Home page first.")
        return None, []

    privacy_df = df.copy()
    privacy_logs = []

    # ── PII Detection Banner ──
    pii_keywords = ['email', 'phone', 'name', 'address', 'ssn', 'id', 'ip', 'passport', 'dob', 'birth', 'credit', 'card']
    potential_pii = [c for c in privacy_df.columns if any(k in c.lower() for k in pii_keywords)]

    if potential_pii:
        pii_list = "".join([f"<span style='background:rgba(239,68,68,0.15); color:#F87171; border:1px solid rgba(239,68,68,0.3); border-radius:6px; padding:3px 10px; margin:3px; display:inline-block; font-size:0.82rem;'>⚠️ {c}</span>" for c in potential_pii])
        st.markdown(f"""
        <div style="background:rgba(239,68,68,0.06); border:1px solid rgba(239,68,68,0.2);
            border-radius:16px; padding:20px 24px; margin-bottom:20px;">
            <div style="font-weight:700; color:#F87171; font-size:1rem; margin-bottom:10px;">
                🔍 {len(potential_pii)} PII Column(s) Auto-Detected
            </div>
            <div style="display:flex; flex-wrap:wrap; gap:4px;">{pii_list}</div>
            <div style="color:#64748B; font-size:0.78rem; margin-top:10px;">
                Detected by scanning column names for sensitive keywords. Review and confirm below.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(34,197,94,0.06); border:1px solid rgba(34,197,94,0.2);
            border-radius:14px; padding:18px 22px; margin-bottom:20px;">
            ✅ <b style="color:#22C55E;">No obvious PII detected</b> based on column names.
            You can still manually select columns below.
        </div>
        """, unsafe_allow_html=True)

    # ── Controls ──
    c1, c2 = st.columns([2, 1])
    with c1:
        pii_cols = st.multiselect("Select columns to anonymize", df.columns.tolist(),
                                   default=potential_pii, key="pii_cols")
    with c2:
        action = st.radio("Anonymization Method", [
            "🔐 Hash (SHA-256)",
            "🗑️ Drop Column"
        ], key="pii_action")

    if pii_cols:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.07);
            border-radius:12px; padding:14px 20px; margin:14px 0; color:#94A3B8; font-size:0.85rem;">
            📋 Preview of selected columns before anonymization:
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(privacy_df[pii_cols].head(5), use_container_width=True)

    if st.button("🛡️ Apply Anonymization", type="primary") and pii_cols:
        for col in pii_cols:
            if "Drop" in action:
                privacy_df.drop(columns=[col], inplace=True)
                privacy_logs.append(f"Dropped PII column '{col}'.")
            else:
                privacy_df[col] = privacy_df[col].astype(str).apply(
                    lambda x: hashlib.sha256(x.encode()).hexdigest()[:16] + "..." if pd.notnull(x) else x
                )
                privacy_logs.append(f"SHA-256 hashed PII column '{col}'.")

        st.markdown(f"""
        <div style="background:rgba(34,197,94,0.08); border:1px solid rgba(34,197,94,0.25);
            border-radius:14px; padding:18px 22px; margin-top:16px;">
            <div style="font-weight:700; color:#22C55E; margin-bottom:10px;">
                ✅ Anonymization Complete — {len(pii_cols)} column(s) processed
            </div>
            {"".join([f"<div style='color:#94A3B8; font-size:0.83rem; padding:2px 0;'>• {l}</div>" for l in privacy_logs])}
        </div>
        """, unsafe_allow_html=True)

        if "Hash" in action:
            remaining = [c for c in pii_cols if c in privacy_df.columns]
            if remaining:
                st.markdown("**Preview of hashed values:**")
                st.dataframe(privacy_df[remaining].head(5), use_container_width=True)

    return privacy_df, privacy_logs
