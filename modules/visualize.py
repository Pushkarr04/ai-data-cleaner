import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from modules.ui import PREMIUM_CSS, section_header

# ── Shared dark chart theme ──
CHART_LAYOUT = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#E2E8F0', family='Outfit, sans-serif'),
    title_font=dict(size=15, color='#E2E8F0'),
    legend=dict(bgcolor='rgba(255,255,255,0.05)', bordercolor='rgba(255,255,255,0.1)', borderwidth=1),
    xaxis=dict(gridcolor='rgba(255,255,255,0.06)', zerolinecolor='rgba(255,255,255,0.08)'),
    yaxis=dict(gridcolor='rgba(255,255,255,0.06)', zerolinecolor='rgba(255,255,255,0.08)'),
    margin=dict(t=50, b=40, l=40, r=20),
)

RAW_COLOR   = '#EF4444'
CLEAN_COLOR = '#22C55E'

def _apply(fig, **kw):
    fig.update_layout(**CHART_LAYOUT, **kw)
    return fig

def _badge_html(label, value, delta, lower_is_better=True):
    """Return a single summary badge card as HTML string.
    All Python logic done here — no ternaries inside the HTML string."""
    if lower_is_better:
        color = '#22C55E' if delta < 0 else ('#EF4444' if delta > 0 else '#64748B')
    else:
        color = '#22C55E' if delta > 0 else ('#EF4444' if delta < 0 else '#64748B')
    arrow = '▼' if delta < 0 else ('▲' if delta > 0 else '=')
    abs_d = abs(delta)
    return (
        f'<div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.08);'
        f'border-radius:10px; padding:12px 16px; text-align:center; flex:1; min-width:120px;">'
        f'<div style="color:#64748B; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">{label}</div>'
        f'<div style="font-size:1.3rem; font-weight:800; color:#E2E8F0;">{value:,}</div>'
        f'<div style="font-size:0.8rem; color:{color}; font-weight:600; margin-top:2px;">{arrow} {abs_d:,} vs raw</div>'
        f'</div>'
    )


def show_visualizations(raw_df, cleaned_df):
    st.markdown(PREMIUM_CSS, unsafe_allow_html=True)
    section_header("📊", "Interactive Visualizations",
                   "Every chart shows Raw (🔴) vs Cleaned (🟢) so you can see exactly what changed.")

    if raw_df is None or cleaned_df is None:
        st.markdown(
            '<div style="text-align:center; padding:60px 20px; background:rgba(255,255,255,0.02);'
            'border:1px dashed rgba(255,255,255,0.08); border-radius:18px;">'
            '<div style="font-size:3rem;">📊</div>'
            '<div style="color:#E2E8F0; font-weight:700; margin-top:12px;">No dataset loaded</div>'
            '<div style="color:#64748B; font-size:0.85rem; margin-top:6px;">Upload a dataset on the Home page first.</div>'
            '</div>',
            unsafe_allow_html=True)
        return

    # ── Pre-compute all badge values (no expressions inside HTML strings) ──
    r_miss = int(raw_df.isnull().sum().sum())
    c_miss = int(cleaned_df.isnull().sum().sum())
    r_dups = int(raw_df.duplicated().sum())
    c_dups = int(cleaned_df.duplicated().sum())
    r_rows = len(raw_df)
    c_rows = len(cleaned_df)
    r_cols = len(raw_df.columns)
    c_cols = len(cleaned_df.columns)

    row_delta  = c_rows - r_rows
    col_delta  = c_cols - r_cols

    badges_html = (
        _badge_html("Missing Cells",  c_miss, c_miss - r_miss, lower_is_better=True) +
        _badge_html("Duplicate Rows", c_dups, c_dups - r_dups, lower_is_better=True) +
        _badge_html("Total Rows",     c_rows, row_delta,        lower_is_better=True) +
        _badge_html("Columns",        c_cols, col_delta,        lower_is_better=False)
    )

    st.markdown(
        '<div style="background:linear-gradient(135deg,rgba(79,172,254,0.07),rgba(0,242,254,0.03));'
        'border:1px solid rgba(0,242,254,0.18); border-radius:16px; padding:18px 22px; margin-bottom:20px;">'
        '<div style="font-size:0.78rem; color:#64748B; text-transform:uppercase; letter-spacing:2px; margin-bottom:12px;">'
        '📊 Dataset Comparison Summary'
        '</div>'
        f'<div style="display:flex; gap:12px; flex-wrap:wrap;">{badges_html}</div>'
        '<div style="margin-top:10px; font-size:0.75rem; color:#64748B;">'
        '🔴 Red = Raw/Before &nbsp;&nbsp; 🟢 Green = Cleaned/After'
        '</div>'
        '</div>',
        unsafe_allow_html=True)

    # ── Column lists ──
    num_raw    = raw_df.select_dtypes(include='number').columns.tolist()
    num_clean  = cleaned_df.select_dtypes(include='number').columns.tolist()
    num_common = [c for c in num_raw if c in num_clean]

    cat_raw    = raw_df.select_dtypes(include=['object', 'category']).columns.tolist()
    cat_clean  = cleaned_df.select_dtypes(include=['object', 'category']).columns.tolist()
    cat_common = [c for c in cat_raw if c in cat_clean]

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "❓ Missing Values", "📈 Distributions", "🔥 Correlation",
        "🔵 2D Scatter", "📦 Box Plots", "🏷️ Categories", "🌐 3D Scatter"
    ])

    # ───────────────────────────────────────
    #  TAB 1 — Missing Values
    # ───────────────────────────────────────
    with tab1:
        try:
            miss_raw   = raw_df.isnull().sum()
            miss_clean = cleaned_df.isnull().sum()
            cols_with_miss = list(set(
                miss_raw[miss_raw > 0].index.tolist() +
                miss_clean[miss_clean > 0].index.tolist()
            ))

            if not cols_with_miss:
                st.success("✅ No missing values in either dataset!")
            else:
                compare = pd.DataFrame({
                    'Column':  cols_with_miss,
                    'Raw':     [int(miss_raw.get(c, 0))   for c in cols_with_miss],
                    'Cleaned': [int(miss_clean.get(c, 0)) for c in cols_with_miss],
                }).sort_values('Raw', ascending=False)

                fig = go.Figure()
                fig.add_trace(go.Bar(name='🔴 Raw',     x=compare['Column'], y=compare['Raw'],
                                     marker_color=RAW_COLOR,   opacity=0.85))
                fig.add_trace(go.Bar(name='🟢 Cleaned', x=compare['Column'], y=compare['Cleaned'],
                                     marker_color=CLEAN_COLOR, opacity=0.85))
                _apply(fig, title='Missing Values per Column — Before vs After',
                       barmode='group', height=380)
                st.plotly_chart(fig, use_container_width=True)

                compare['Resolved']     = compare['Raw'] - compare['Cleaned']
                compare['Raw %']        = (compare['Raw']     / r_rows * 100).round(1)
                compare['Cleaned %']    = (compare['Cleaned'] / c_rows * 100).round(1)
                st.dataframe(compare.reset_index(drop=True), use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Missing Values tab error: {e}")

    # ───────────────────────────────────────
    #  TAB 2 — Distributions
    # ───────────────────────────────────────
    with tab2:
        try:
            if not num_common:
                st.info("No common numeric columns between raw and cleaned datasets.")
            else:
                col_sel  = st.selectbox("Select column", num_common, key="dist_col")
                show_kde = st.checkbox("Show KDE density curve", value=True, key="dist_kde")

                fig = go.Figure()
                for src, label, color in [(raw_df, "🔴 Raw", RAW_COLOR),
                                           (cleaned_df, "🟢 Cleaned", CLEAN_COLOR)]:
                    data = src[col_sel].dropna().astype(float)
                    fig.add_trace(go.Histogram(x=data, name=label, opacity=0.55,
                                               marker_color=color, nbinsx=40))
                    if show_kde and len(data) > 5:
                        try:
                            from scipy import stats as sp
                            x_r = np.linspace(float(data.min()), float(data.max()), 300)
                            kde = sp.gaussian_kde(data)
                            bw  = (data.max() - data.min()) / 40 if data.max() != data.min() else 1
                            fig.add_trace(go.Scatter(
                                x=x_r, y=kde(x_r) * len(data) * bw,
                                name=label + " KDE",
                                line=dict(color=color, width=2.5, dash='dot')))
                        except Exception:
                            pass

                fig.update_layout(barmode='overlay')
                _apply(fig, title=f"Distribution: {col_sel}")
                st.plotly_chart(fig, use_container_width=True)

                # Stats comparison table
                s_raw   = raw_df[col_sel].describe().round(3)
                s_clean = cleaned_df[col_sel].describe().round(3)
                stats   = pd.DataFrame({
                    'Statistic': s_raw.index,
                    'Raw':       s_raw.values,
                    'Cleaned':   s_clean.values,
                })
                stats['Changed'] = stats.apply(
                    lambda r: '✅ Yes' if r['Raw'] != r['Cleaned'] else '—', axis=1)
                st.dataframe(stats, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Distributions tab error: {e}")

    # ───────────────────────────────────────
    #  TAB 3 — Correlation Heatmap
    # ───────────────────────────────────────
    with tab3:
        try:
            method = st.radio("Correlation method", ["pearson", "spearman"],
                              horizontal=True, key="corr_m")

            num_df_r = raw_df.select_dtypes(include='number')
            num_df_c = cleaned_df.select_dtypes(include='number')

            if len(num_df_r.columns) < 2 and len(num_df_c.columns) < 2:
                st.info("Need at least 2 numeric columns.")
            else:
                corr_r = num_df_r.corr(method=method).round(2)
                corr_c = num_df_c.corr(method=method).round(2)

                fig = make_subplots(rows=1, cols=2,
                                    subplot_titles=["🔴 Raw Correlation",
                                                    "🟢 Cleaned Correlation"])
                fig.add_trace(go.Heatmap(
                    z=corr_r.values, x=corr_r.columns.tolist(), y=corr_r.index.tolist(),
                    colorscale='RdBu_r', zmin=-1, zmax=1,
                    text=corr_r.values.round(2), texttemplate='%{text}',
                    showscale=False), row=1, col=1)
                fig.add_trace(go.Heatmap(
                    z=corr_c.values, x=corr_c.columns.tolist(), y=corr_c.index.tolist(),
                    colorscale='RdBu_r', zmin=-1, zmax=1,
                    text=corr_c.values.round(2), texttemplate='%{text}',
                    showscale=True), row=1, col=2)
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#E2E8F0'), height=500,
                    title=f"{method.title()} Correlation — Raw vs Cleaned")
                st.plotly_chart(fig, use_container_width=True)

                # Delta heatmap
                common_c = [c for c in corr_r.columns if c in corr_c.columns]
                if len(common_c) >= 2:
                    delta = (corr_c.loc[common_c, common_c] -
                             corr_r.loc[common_c, common_c]).round(3)
                    fig2 = go.Figure(go.Heatmap(
                        z=delta.values,
                        x=delta.columns.tolist(),
                        y=delta.index.tolist(),
                        colorscale='PiYG', zmin=-1, zmax=1,
                        text=delta.values, texttemplate='%{text}',
                    ))
                    _apply(fig2, title="Δ Correlation Change (Cleaned − Raw)", height=380)
                    st.plotly_chart(fig2, use_container_width=True)
        except Exception as e:
            st.error(f"Correlation tab error: {e}")

    # ───────────────────────────────────────
    #  TAB 4 — 2D Scatter
    # ───────────────────────────────────────
    with tab4:
        try:
            if len(num_common) < 2:
                st.info("Need at least 2 common numeric columns.")
            else:
                c1, c2, c3 = st.columns(3)
                with c1: col_x = st.selectbox("X-axis", num_common, index=0, key="sx")
                with c2: col_y = st.selectbox("Y-axis", num_common,
                                               index=min(1, len(num_common)-1), key="sy")
                with c3: color_col = st.selectbox("Color by", ["None"] + cat_raw, key="sc")

                plot_color = None if color_col == "None" else color_col

                fig = make_subplots(rows=1, cols=2,
                                    subplot_titles=["🔴 Raw Dataset", "🟢 Cleaned Dataset"])

                for col_idx, (src, label, color) in enumerate(
                        [(raw_df, "Raw", RAW_COLOR), (cleaned_df, "Cleaned", CLEAN_COLOR)], 1):
                    if col_x in src.columns and col_y in src.columns:
                        if plot_color and plot_color in src.columns:
                            for i, cat in enumerate(src[plot_color].dropna().unique()):
                                mask = src[plot_color].astype(str) == str(cat)
                                fig.add_trace(go.Scatter(
                                    x=src.loc[mask, col_x], y=src.loc[mask, col_y],
                                    mode='markers', name=str(cat),
                                    marker=dict(
                                        color=px.colors.qualitative.Vivid[i % len(px.colors.qualitative.Vivid)],
                                        size=5, opacity=0.6),
                                    showlegend=(col_idx == 1)
                                ), row=1, col=col_idx)
                        else:
                            plot_df = src[[col_x, col_y]].dropna()
                            fig.add_trace(go.Scatter(
                                x=plot_df[col_x], y=plot_df[col_y],
                                mode='markers', name=label,
                                marker=dict(color=color, size=5, opacity=0.6)
                            ), row=1, col=col_idx)

                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#E2E8F0'), height=430,
                    title=f"Scatter: {col_x} vs {col_y}")
                st.plotly_chart(fig, use_container_width=True)

                r_pts = int(raw_df[[col_x, col_y]].dropna().shape[0])
                c_pts = int(cleaned_df[[col_x, col_y]].dropna().shape[0])
                st.markdown(
                    f'<div style="color:#64748B; font-size:0.82rem;">'
                    f'Valid points — Raw: <b style="color:{RAW_COLOR}">{r_pts:,}</b>'
                    f' &nbsp;|&nbsp; '
                    f'Cleaned: <b style="color:{CLEAN_COLOR}">{c_pts:,}</b>'
                    f'</div>',
                    unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Scatter tab error: {e}")

    # ───────────────────────────────────────
    #  TAB 5 — Box Plots
    # ───────────────────────────────────────
    with tab5:
        try:
            if not num_common:
                st.info("No common numeric columns.")
            else:
                c1, c2 = st.columns(2)
                with c1: box_col   = st.selectbox("Column", num_common, key="bc")
                with c2: group_col = st.selectbox("Group by", ["None"] + cat_common, key="bg")

                if group_col != "None":
                    fig = make_subplots(rows=1, cols=2,
                                        subplot_titles=["🔴 Raw", "🟢 Cleaned"])
                    for col_idx, (src, _) in enumerate(
                            [(raw_df, "Raw"), (cleaned_df, "Cleaned")], 1):
                        if box_col in src.columns and group_col in src.columns:
                            for grp in src[group_col].dropna().unique():
                                fig.add_trace(go.Box(
                                    y=src[src[group_col] == grp][box_col].dropna(),
                                    name=str(grp), boxmean=True,
                                    showlegend=(col_idx == 1)
                                ), row=1, col=col_idx)
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#E2E8F0'), height=450,
                        title=f"Box: {box_col} grouped by {group_col}")
                else:
                    fig = go.Figure()
                    for src, label, color in [
                            (raw_df, "🔴 Raw", RAW_COLOR),
                            (cleaned_df, "🟢 Cleaned", CLEAN_COLOR)]:
                        if box_col in src.columns:
                            fig.add_trace(go.Box(
                                y=src[box_col].dropna(), name=label,
                                marker_color=color, boxmean=True))
                    _apply(fig, title=f"Box Plot: {box_col}", height=420)

                st.plotly_chart(fig, use_container_width=True)

                # Stats row per dataset
                for label, src, color in [
                        ("Raw",     raw_df,     RAW_COLOR),
                        ("Cleaned", cleaned_df, CLEAN_COLOR)]:
                    if box_col in src.columns:
                        d = src[box_col].dropna()
                        Q1, Q3 = float(d.quantile(0.25)), float(d.quantile(0.75))
                        IQR = Q3 - Q1
                        outs = int(((d < Q1 - 1.5*IQR) | (d > Q3 + 1.5*IQR)).sum())
                        mean_v   = round(float(d.mean()), 2)
                        median_v = round(float(d.median()), 2)
                        std_v    = round(float(d.std()), 2)
                        st.markdown(
                            f'<div style="margin-top:6px; font-size:0.83rem;">'
                            f'<span style="color:{color}; font-weight:700;">{label}</span>'
                            f'<span style="color:#64748B;"> — '
                            f'Mean: <b style="color:#E2E8F0">{mean_v}</b> · '
                            f'Median: <b style="color:#E2E8F0">{median_v}</b> · '
                            f'Std: <b style="color:#E2E8F0">{std_v}</b> · '
                            f'Outliers: <b style="color:#F59E0B">{outs:,}</b>'
                            f'</span></div>',
                            unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Box plot tab error: {e}")

    # ───────────────────────────────────────
    #  TAB 6 — Categories
    # ───────────────────────────────────────
    with tab6:
        try:
            if not cat_common:
                st.info("No categorical columns available (they may have been encoded to numeric).")
            else:
                c1, c2 = st.columns(2)
                with c1: cat_col    = st.selectbox("Column", cat_common, key="cc")
                with c2: chart_mode = st.radio("Chart type",
                                                ["Side-by-Side Bars", "Pie", "Treemap"],
                                                horizontal=True, key="cc_mode")

                top_n = st.slider("Top N categories", 5, 30, 15, key="cc_n")

                vc_raw   = raw_df[cat_col].value_counts().head(top_n)
                vc_clean = cleaned_df[cat_col].value_counts().head(top_n)
                all_cats = list(dict.fromkeys(
                    list(vc_raw.index.astype(str)) + list(vc_clean.index.astype(str))
                ))
                raw_vals   = [int(vc_raw.get(c, 0))   for c in all_cats]
                clean_vals = [int(vc_clean.get(c, 0)) for c in all_cats]

                if chart_mode == "Side-by-Side Bars":
                    fig = go.Figure()
                    fig.add_trace(go.Bar(name='🔴 Raw',     x=all_cats, y=raw_vals,
                                         marker_color=RAW_COLOR,   opacity=0.85))
                    fig.add_trace(go.Bar(name='🟢 Cleaned', x=all_cats, y=clean_vals,
                                         marker_color=CLEAN_COLOR, opacity=0.85))
                    _apply(fig, title=f"Category Counts: {cat_col}",
                           barmode='group', height=400)
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_mode == "Pie":
                    fig = make_subplots(
                        rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'pie'}]],
                        subplot_titles=["🔴 Raw", "🟢 Cleaned"])
                    fig.add_trace(go.Pie(
                        labels=list(vc_raw.index.astype(str)), values=vc_raw.values,
                        marker_colors=px.colors.qualitative.Pastel), row=1, col=1)
                    fig.add_trace(go.Pie(
                        labels=list(vc_clean.index.astype(str)), values=vc_clean.values,
                        marker_colors=px.colors.qualitative.Vivid), row=1, col=2)
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#E2E8F0'), height=420)
                    st.plotly_chart(fig, use_container_width=True)

                else:  # Treemap
                    fig = make_subplots(
                        rows=1, cols=2,
                        specs=[[{'type': 'treemap'}, {'type': 'treemap'}]],
                        subplot_titles=["🔴 Raw", "🟢 Cleaned"])
                    fig.add_trace(go.Treemap(
                        labels=list(vc_raw.index.astype(str)),
                        parents=['']*len(vc_raw), values=vc_raw.values), row=1, col=1)
                    fig.add_trace(go.Treemap(
                        labels=list(vc_clean.index.astype(str)),
                        parents=['']*len(vc_clean), values=vc_clean.values), row=1, col=2)
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#E2E8F0'), height=420)
                    st.plotly_chart(fig, use_container_width=True)

                # Changed categories table
                diff = pd.DataFrame({
                    'Category':      all_cats,
                    'Raw Count':     raw_vals,
                    'Cleaned Count': clean_vals,
                })
                diff['Δ Change'] = diff['Cleaned Count'] - diff['Raw Count']
                changed = diff[diff['Δ Change'] != 0]
                if not changed.empty:
                    st.markdown(
                        '<div style="color:#94A3B8; font-size:0.82rem; margin-top:8px;">'
                        'Categories that changed:</div>',
                        unsafe_allow_html=True)
                    st.dataframe(changed.reset_index(drop=True),
                                 use_container_width=True, hide_index=True)
                else:
                    st.markdown(
                        '<div style="color:#64748B; font-size:0.82rem; margin-top:8px;">'
                        'No category counts changed between raw and cleaned.</div>',
                        unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Categories tab error: {e}")

    # ───────────────────────────────────────
    #  TAB 7 — 3D Scatter
    # ───────────────────────────────────────
    with tab7:
        try:
            if len(num_common) < 3:
                st.info(f"Need at least 3 common numeric columns. Currently: {len(num_common)}.")
            else:
                c1, c2, c3, c4 = st.columns(4)
                with c1: x3  = st.selectbox("X", num_common, index=0, key="x3")
                with c2: y3  = st.selectbox("Y", num_common, index=min(1, len(num_common)-1), key="y3")
                with c3: z3  = st.selectbox("Z", num_common, index=min(2, len(num_common)-1), key="z3")
                with c4: c3d = st.selectbox("Color by", ["None"] + cat_common + num_common, key="c3d")

                view_mode = st.radio("View mode", ["🔴 Raw Only", "🟢 Cleaned Only", "⚡ Side-by-Side"],
                                     horizontal=True, key="v3d")

                color_col_3d = None if c3d == "None" else c3d

                def _make_3d(src, title_label):
                    needed = [x3, y3, z3] + ([color_col_3d] if color_col_3d and color_col_3d in src.columns else [])
                    needed = [c for c in needed if c in src.columns]
                    plot   = src[needed].dropna()
                    clr    = plot[color_col_3d] if color_col_3d and color_col_3d in plot.columns else None
                    f = px.scatter_3d(plot, x=x3, y=y3, z=z3, color=clr,
                                      opacity=0.72, title=f"3D Scatter — {title_label}",
                                      color_discrete_sequence=px.colors.qualitative.Vivid)
                    f.update_traces(marker=dict(size=4))
                    f.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#E2E8F0'),
                        margin=dict(l=0, r=0, b=0, t=45),
                        scene=dict(
                            xaxis=dict(backgroundcolor='rgba(0,0,0,0)',
                                       gridcolor='rgba(255,255,255,0.08)'),
                            yaxis=dict(backgroundcolor='rgba(0,0,0,0)',
                                       gridcolor='rgba(255,255,255,0.08)'),
                            zaxis=dict(backgroundcolor='rgba(0,0,0,0)',
                                       gridcolor='rgba(255,255,255,0.08)'),
                        ))
                    return f

                if "Side-by-Side" in view_mode:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(
                            '<div style="text-align:center; color:#EF4444; font-weight:700; margin-bottom:4px;">🔴 Raw</div>',
                            unsafe_allow_html=True)
                        st.plotly_chart(_make_3d(raw_df, "Raw"), use_container_width=True)
                    with col_b:
                        st.markdown(
                            '<div style="text-align:center; color:#22C55E; font-weight:700; margin-bottom:4px;">🟢 Cleaned</div>',
                            unsafe_allow_html=True)
                        st.plotly_chart(_make_3d(cleaned_df, "Cleaned"), use_container_width=True)
                elif "Raw" in view_mode:
                    st.plotly_chart(_make_3d(raw_df, "Raw"), use_container_width=True)
                else:
                    st.plotly_chart(_make_3d(cleaned_df, "Cleaned"), use_container_width=True)

        except Exception as e:
            st.error(f"3D Scatter tab error: {e}")
