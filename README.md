# 🧹 DataCleaner AI — Enterprise Edition

> **AI-powered data cleaning, transformation, visualization & export platform built with Streamlit.**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.5%2B-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Module | Capabilities |
|---|---|
| 🏠 **Home** | Upload CSV/Excel, live dataset health score, AI insights |
| 🔍 **Data Overview** | Column types, missing values, distributions, quality score |
| 🧹 **Smart Cleaning** | ML-based imputation (KNN, Mean, Median, Mode), duplicate removal, outlier treatment, text cleaning, date/time extraction |
| 🛡️ **Data Privacy** | Auto PII detection (email, phone, name), hashing & anonymization |
| ⚙️ **Transformations** | Min-Max / Standard scaling, One-Hot / Label encoding, feature engineering |
| 📊 **Visualizations** | 7 chart types — all showing Raw 🔴 vs Cleaned 🟢 side-by-side |
| 💻 **Code Generator** | Auto-generates a reproducible Python cleaning pipeline script |
| 🆚 **Compare & Export** | Before/after comparison, CSV/Excel export |

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/DataCleaner-AI.git
cd DataCleaner-AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 📦 Requirements

```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.24.0
plotly>=5.13.0
scikit-learn>=1.2.0
scipy>=1.10.0
openpyxl>=3.1.0
```

---

## 📁 Project Structure

```
DataCleaner_AI/
├── app.py                    ← Main landing page
├── requirements.txt
├── test_dataset.csv          ← Sample dataset to test all features
│
├── modules/                  ← Core logic modules
│   ├── ui.py                 ← Shared CSS & UI components
│   ├── upload.py             ← File upload handler
│   ├── cleaner.py            ← Smart cleaning engine
│   ├── quality.py            ← Data quality analysis
│   ├── transform.py          ← Scaling & encoding
│   ├── privacy.py            ← PII detection & anonymization
│   ├── visualize.py          ← Interactive charts
│   ├── comparison.py         ← Before/after comparison & export
│   └── code_generator.py    ← Pipeline code generation
│
├── pages/                    ← Streamlit multi-page navigation
│   ├── 1_Data_Overview.py
│   ├── 2_Smart_Cleaning.py
│   ├── 3_Data_Privacy.py
│   ├── 4_Transformations.py
│   ├── 5_Visualizations.py
│   ├── 6_Code_Generator.py
│   └── 7_Compare_and_Export.py
│
└── utils/
    ├── ai_suggestions.py     ← Quality scoring & imputation hints
    └── insights.py           ← Automated dataset insights
```

---

## 🎯 Test Dataset

Upload `test_dataset.csv` (included) to test all features:
- **315 rows × 20 columns**
- PII columns: `full_name`, `email`, `phone`
- Missing values: `age` (16%), `department` (11%), `score_1` (7%)
- 15 duplicate rows
- Outliers in `salary` and `score_1`
- HTML/URL text in `feedback` column
- Date columns: `join_date`, `last_review_date`

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit + Plotly + Custom CSS (Glassmorphism / Deep Space theme)
- **ML**: scikit-learn (KNN Imputer), scipy (KDE)
- **Data**: pandas, numpy
- **Export**: openpyxl (Excel), CSV

---

## 📄 License

MIT License — free to use, modify, and distribute.
