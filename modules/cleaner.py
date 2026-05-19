import streamlit as st
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from utils.ai_suggestions import suggest_missing_value_strategy
from modules.ui import PREMIUM_CSS, section_header

def show_cleaning_options(df):
    st.markdown(PREMIUM_CSS, unsafe_allow_html=True)
    section_header("🧹", "Smart Cleaning & Imputation (Enterprise)",
                   "Apply ML-powered cleaning operations on your dataset.")

    if df is None:
        st.info("Please upload a dataset first.")
        return None, []

    cleaned_df = df.copy()
    cleaning_logs = []

    # ── One-Click Pipeline ──
    st.markdown("""
    <div style="background:rgba(0,242,254,0.05); border:1px solid rgba(0,242,254,0.2);
        border-radius:14px; padding:16px 20px; margin-bottom:20px;">
        <div style="font-weight:700; color:#E2E8F0; margin-bottom:4px;">⚡ One-Click Auto Mode</div>
        <div style="color:#64748B; font-size:0.83rem;">
            Automatically fills all missing values, removes duplicates and converts types.
        </div>
    </div>
    """, unsafe_allow_html=True)
    pipeline_mode = st.button("🚀 One-Click Clean Entire Dataset (Auto Mode)", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "❓ Missing Values", "🗂️ Duplicates & Types", "📉 Outliers", "🔤 Text Cleaning", "📅 Date/Time"
    ])

    # ─────────────────────────────────────────────
    #  TAB 1 — Missing Values
    # ─────────────────────────────────────────────
    with tab1:
        section_header("❓", "Enterprise Imputation Engine",
                       "Handle missing values per column using statistical or ML methods.")

        missing_cols = cleaned_df.columns[cleaned_df.isnull().any()].tolist()

        if not missing_cols:
            st.markdown("""
            <div style="text-align:center; padding:30px; background:rgba(34,197,94,0.06);
                border:1px solid rgba(34,197,94,0.2); border-radius:14px;">
                <div style="font-size:2rem;">✅</div>
                <div style="color:#22C55E; font-weight:700; margin-top:8px;">No missing values found!</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color:#94A3B8; font-size:0.85rem; margin-bottom:16px;'>"
                        f"Found <b style='color:#F59E0B'>{len(missing_cols)}</b> column(s) with missing values.</div>",
                        unsafe_allow_html=True)

            for col in missing_cols:
                col_type = cleaned_df[col].dtype
                missing_count = int(cleaned_df[col].isnull().sum())
                missing_pct = missing_count / len(cleaned_df) * 100

                bar_color = "#EF4444" if missing_pct > 30 else "#F59E0B" if missing_pct > 10 else "#00F2FE"

                # Custom card — NO st.expander to avoid arrow_right bleed
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.08);
                    border-radius:12px; padding:14px 18px; margin-bottom:10px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <div>
                            <span style="font-weight:700; color:#E2E8F0; font-size:0.95rem;">{col}</span>
                            <span style="color:#64748B; font-size:0.78rem; margin-left:10px;">
                                {missing_count:,} missing · {missing_pct:.1f}%
                            </span>
                        </div>
                        <span style="color:{bar_color}; font-size:0.78rem; font-weight:700;">
                            {'🔴 High' if missing_pct > 30 else '🟡 Medium' if missing_pct > 10 else '🟢 Low'}
                        </span>
                    </div>
                    <div style="background:rgba(255,255,255,0.05); border-radius:50px; height:4px; margin-bottom:12px;">
                        <div style="width:{min(missing_pct, 100):.1f}%; height:4px; border-radius:50px;
                            background:{bar_color};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Controls directly (no expander)
                with st.container():
                    try:
                        suggestion = suggest_missing_value_strategy(cleaned_df, col)
                        st.markdown(f"<div style='color:#64748B; font-size:0.8rem; margin:-8px 0 8px 4px;'>"
                                    f"💡 AI Suggestion: <b style='color:#00F2FE'>{suggestion}</b></div>",
                                    unsafe_allow_html=True)
                    except Exception:
                        suggestion = "Mean" if pd.api.types.is_numeric_dtype(col_type) else "Mode"

                    is_numeric = pd.api.types.is_numeric_dtype(col_type)
                    options = ["— Select method —", "Mean", "Median", "KNN Imputer (ML)", "Drop Rows"] if is_numeric \
                              else ["— Select method —", "Mode", "Fill 'Unknown'", "Drop Rows"]

                    method = st.selectbox("", options, key=f"miss_{col}", label_visibility="collapsed")

                    if pipeline_mode:
                        method = "Mean" if is_numeric else "Mode"

                    if method not in ["— Select method —", None]:
                        try:
                            if method == "Mean":
                                cleaned_df[col].fillna(cleaned_df[col].mean(), inplace=True)
                                cleaning_logs.append(f"Filled missing values in '{col}' with Mean.")
                            elif method == "Median":
                                cleaned_df[col].fillna(cleaned_df[col].median(), inplace=True)
                                cleaning_logs.append(f"Filled missing values in '{col}' with Median.")
                            elif method == "KNN Imputer (ML)":
                                with st.spinner(f"KNN Imputing '{col}'..."):
                                    imputer = KNNImputer(n_neighbors=5)
                                    num_df = cleaned_df.select_dtypes(include=['number'])
                                    imputed = imputer.fit_transform(num_df)
                                    col_idx = num_df.columns.get_loc(col)
                                    cleaned_df[col] = imputed[:, col_idx]
                                cleaning_logs.append(f"Applied KNN Imputation to '{col}'.")
                            elif method == "Mode":
                                cleaned_df[col].fillna(cleaned_df[col].mode()[0], inplace=True)
                                cleaning_logs.append(f"Filled missing values in '{col}' with Mode.")
                            elif method == "Fill 'Unknown'":
                                cleaned_df[col].fillna("Unknown", inplace=True)
                                cleaning_logs.append(f"Filled missing values in '{col}' with 'Unknown'.")
                            elif method == "Drop Rows":
                                cleaned_df.dropna(subset=[col], inplace=True)
                                cleaning_logs.append(f"Dropped rows with missing values in '{col}'.")
                        except Exception as e:
                            st.error(f"Error handling '{col}': {e}")

                st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    #  TAB 2 — Duplicates & Types
    # ─────────────────────────────────────────────
    with tab2:
        c1, c2 = st.columns(2)

        with c1:
            section_header("🗂️", "Duplicate Rows")
            dups = int(cleaned_df.duplicated().sum())
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.07);
                border-radius:12px; padding:16px 20px; margin-bottom:12px;">
                <div style="font-size:2rem; font-weight:800; color:{'#EF4444' if dups > 0 else '#22C55E'};">
                    {dups:,}
                </div>
                <div style="color:#64748B; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">
                    Duplicate rows found
                </div>
            </div>
            """, unsafe_allow_html=True)

            if dups > 0:
                remove_dup = st.checkbox("✅ Remove all duplicate rows", value=pipeline_mode, key="rm_dup")
                if remove_dup:
                    cleaned_df.drop_duplicates(inplace=True)
                    cleaning_logs.append(f"Removed {dups} duplicate rows.")
                    st.success(f"Removed {dups} duplicates.")
            else:
                st.success("No duplicates found!")

        with c2:
            section_header("🏷️", "Data Type Correction")
            auto_convert = st.checkbox("Auto-convert text columns that contain numbers",
                                       value=pipeline_mode, key="auto_conv")
            if auto_convert:
                converted = []
                for col in cleaned_df.columns:
                    if cleaned_df[col].dtype == 'object':
                        try:
                            cleaned_df[col] = pd.to_numeric(cleaned_df[col])
                            converted.append(col)
                            cleaning_logs.append(f"Converted column '{col}' to numeric type.")
                        except (ValueError, TypeError):
                            pass
                if converted:
                    st.success(f"Converted {len(converted)} column(s): {', '.join(converted)}")
                else:
                    st.info("No convertible columns found.")

            st.markdown("**Current Data Types**")
            dtype_df = pd.DataFrame({
                'Column': cleaned_df.columns,
                'Type': cleaned_df.dtypes.astype(str).values
            })
            st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    # ─────────────────────────────────────────────
    #  TAB 3 — Outliers
    # ─────────────────────────────────────────────
    with tab3:
        section_header("📉", "Outlier Handling", "Uses the IQR method to detect and treat outliers.")
        num_cols = cleaned_df.select_dtypes(include=['number']).columns.tolist()

        if not num_cols:
            st.info("No numerical columns available.")
        else:
            col_a, col_b = st.columns(2)
            with col_a:
                outlier_cols = st.multiselect("Select columns to treat", num_cols, key="out_cols")
            with col_b:
                outlier_method = st.radio("Treatment method",
                                          ["Capping (IQR bounds)", "Remove rows"],
                                          horizontal=True, key="out_method")

            if outlier_cols:
                # Show outlier summary per column
                for col in outlier_cols:
                    Q1 = cleaned_df[col].quantile(0.25)
                    Q3 = cleaned_df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    outlier_count = int(((cleaned_df[col] < Q1 - 1.5*IQR) | (cleaned_df[col] > Q3 + 1.5*IQR)).sum())
                    st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(245,158,11,0.2);
                        border-radius:10px; padding:12px 16px; margin:6px 0; display:flex;
                        justify-content:space-between; font-size:0.85rem;">
                        <span style="color:#E2E8F0; font-weight:600;">{col}</span>
                        <span style="color:#F59E0B;">{outlier_count:,} outliers detected</span>
                    </div>
                    """, unsafe_allow_html=True)

                if st.button("⚡ Apply Outlier Treatment", key="apply_outlier", type="primary"):
                    for col in outlier_cols:
                        Q1 = cleaned_df[col].quantile(0.25)
                        Q3 = cleaned_df[col].quantile(0.75)
                        IQR = Q3 - Q1
                        lb = Q1 - 1.5 * IQR
                        ub = Q3 + 1.5 * IQR

                        if "Remove" in outlier_method:
                            before = len(cleaned_df)
                            cleaned_df = cleaned_df[(cleaned_df[col] >= lb) & (cleaned_df[col] <= ub)]
                            cleaning_logs.append(f"Removed {before - len(cleaned_df)} outliers from '{col}'.")
                        else:
                            cleaned_df[col] = cleaned_df[col].clip(lower=lb, upper=ub)
                            cleaning_logs.append(f"Capped outliers in '{col}'.")

                    st.success(f"Outlier treatment applied to {len(outlier_cols)} column(s)!")

    # ─────────────────────────────────────────────
    #  TAB 4 — Text Cleaning
    # ─────────────────────────────────────────────
    with tab4:
        section_header("🔤", "NLP Text Cleaning",
                       "Strip HTML tags, URLs, extra whitespace and normalise case.")
        text_cols = cleaned_df.select_dtypes(include=['object']).columns.tolist()

        if not text_cols:
            st.info("No text columns found.")
        else:
            clean_text_cols = st.multiselect("Select columns to clean", text_cols, key="txt_cols")

            ops = st.columns(3)
            with ops[0]: do_lower = st.checkbox("Lowercase", value=True, key="txt_lower")
            with ops[1]: do_html  = st.checkbox("Remove HTML tags", value=True, key="txt_html")
            with ops[2]: do_url   = st.checkbox("Remove URLs", value=True, key="txt_url")

            if clean_text_cols and st.button("⚡ Apply Text Cleaning", key="apply_text", type="primary"):
                for col in clean_text_cols:
                    if do_lower: cleaned_df[col] = cleaned_df[col].astype(str).str.lower()
                    if do_html:  cleaned_df[col] = cleaned_df[col].str.replace(r'<[^>]*>', '', regex=True)
                    if do_url:   cleaned_df[col] = cleaned_df[col].str.replace(r'http\S+|www\.\S+', '', regex=True)
                    cleaned_df[col] = cleaned_df[col].str.strip()
                    cleaning_logs.append(f"Text cleaning applied to '{col}'.")

                st.success(f"Text cleaned on {len(clean_text_cols)} column(s)!")
                st.markdown("**Sample after cleaning:**")
                st.dataframe(cleaned_df[clean_text_cols].head(5), use_container_width=True)

    # ─────────────────────────────────────────────
    #  TAB 5 — Date/Time
    # ─────────────────────────────────────────────
    with tab5:
        section_header("📅", "Date & Time Extraction",
                       "Parse string columns as datetime and extract Year, Month, Day features.")
        all_cols = cleaned_df.columns.tolist()
        potential_date_cols = [c for c in all_cols if any(k in c.lower() for k in ['date', 'time', 'dt', 'day', 'month', 'year'])]

        date_col = st.selectbox(
            "Select column to parse as Date/Time",
            ["— Select column —"] + all_cols,
            index=all_cols.index(potential_date_cols[0]) + 1 if potential_date_cols else 0,
            key="date_col"
        )

        if date_col != "— Select column —":
            sample = cleaned_df[date_col].dropna().head(3).astype(str).tolist()
            st.markdown(f"<div style='color:#64748B; font-size:0.82rem; margin-bottom:12px;'>"
                        f"Sample values: <b style='color:#94A3B8'>{' · '.join(sample)}</b></div>",
                        unsafe_allow_html=True)

            col_f1, col_f2 = st.columns(2)
            with col_f1: extract_ymd = st.checkbox("Extract Year, Month, Day", value=True, key="dt_ymd")
            with col_f2: extract_dow = st.checkbox("Extract Day of Week", value=False, key="dt_dow")

            if st.button("⚡ Apply Date Parsing", key="apply_date", type="primary"):
                try:
                    cleaned_df[date_col] = pd.to_datetime(cleaned_df[date_col], errors='coerce')
                    coerced = cleaned_df[date_col].isnull().sum()

                    if extract_ymd:
                        cleaned_df[f"{date_col}_Year"]  = cleaned_df[date_col].dt.year
                        cleaned_df[f"{date_col}_Month"] = cleaned_df[date_col].dt.month
                        cleaned_df[f"{date_col}_Day"]   = cleaned_df[date_col].dt.day
                    if extract_dow:
                        cleaned_df[f"{date_col}_DayOfWeek"] = cleaned_df[date_col].dt.day_name()

                    cleaning_logs.append(f"Extracted Date/Time features from '{date_col}'.")
                    st.success(f"Date parsing applied! ({coerced} unparseable values → NaT)")
                    st.dataframe(cleaned_df[[date_col] +
                                            ([f"{date_col}_Year", f"{date_col}_Month", f"{date_col}_Day"] if extract_ymd else []) +
                                            ([f"{date_col}_DayOfWeek"] if extract_dow else [])].head(5),
                                 use_container_width=True)
                except Exception as e:
                    st.error(f"Date parsing failed: {e}")

    if pipeline_mode and not cleaning_logs:
        st.info("Auto mode ran — no issues detected in this dataset.")

    return cleaned_df, cleaning_logs
