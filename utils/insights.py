import pandas as pd

def generate_dataset_insights(df):
    """Generates automated text insights about the dataset."""
    insights = []
    
    if df is None or df.empty:
        return ["Dataset is empty."]
        
    # Missing values insights
    missing_percentages = (df.isnull().sum() / len(df)) * 100
    high_missing = missing_percentages[missing_percentages > 20]
    for col, pct in high_missing.items():
        insights.append(f"⚠️ **{col}** has a high percentage of missing values ({pct:.1f}%). Consider dropping it or using advanced imputation.")
        
    # Duplicates insight
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        insights.append(f"🔄 There are **{duplicates}** duplicate rows in the dataset.")
        
    # Skewness insights for numerical columns
    num_cols = df.select_dtypes(include=['number']).columns
    for col in num_cols:
        skew = df[col].skew()
        if skew > 1:
            insights.append(f"📈 **{col}** is highly right-skewed (skewness: {skew:.2f}). Consider log transformation or median imputation.")
        elif skew < -1:
            insights.append(f"📉 **{col}** is highly left-skewed (skewness: {skew:.2f}). Consider transformations.")
            
    # Categorical insights
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in cat_cols:
        unique_count = df[col].nunique()
        if unique_count > len(df) * 0.9:
            insights.append(f"🆔 **{col}** has nearly unique values for each row ({unique_count} unique values). It might be an identifier column.")
        elif unique_count == 1:
            insights.append(f"🧊 **{col}** has only one unique value. It provides no predictive power and can be dropped.")
            
    if not insights:
        insights.append("✅ The dataset looks generally clean and well-structured. No critical issues detected.")
        
    return insights
