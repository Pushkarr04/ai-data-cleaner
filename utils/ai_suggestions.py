def get_data_quality_score(df):
    """Calculate a data quality score from 0 to 100 based on missing values and duplicates."""
    if df is None or df.empty:
        return 0
    
    total_cells = df.size
    total_missing = df.isnull().sum().sum()
    missing_penalty = (total_missing / total_cells) * 50 if total_cells > 0 else 0
    
    total_rows = len(df)
    total_duplicates = df.duplicated().sum()
    duplicate_penalty = (total_duplicates / total_rows) * 50 if total_rows > 0 else 0
    
    score = 100 - missing_penalty - duplicate_penalty
    return max(0, min(100, round(score)))

def suggest_missing_value_strategy(df, column):
    """Suggests a missing value strategy based on column data type and distribution."""
    if df[column].dtype in ['int64', 'float64']:
        skewness = df[column].skew()
        if abs(skewness) > 1:
            return "Median (Data is skewed)"
        else:
            return "Mean (Data is normally distributed)"
    else:
        return "Mode or 'Unknown' (Categorical data)"
