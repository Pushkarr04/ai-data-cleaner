import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def optimize_memory(df):
    """
    Optimizes the memory usage of a pandas DataFrame by downcasting numeric types.
    Uses st.cache_data to avoid re-running on every interaction.
    """
    if df is None:
        return None
        
    initial_memory = df.memory_usage(deep=True).sum() / 1024**2
    optimized_df = df.copy()
    
    for col in optimized_df.columns:
        col_type = optimized_df[col].dtype
        
        if pd.api.types.is_numeric_dtype(col_type):
            c_min = optimized_df[col].min()
            c_max = optimized_df[col].max()
            
            if pd.api.types.is_integer_dtype(col_type):
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    optimized_df[col] = optimized_df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    optimized_df[col] = optimized_df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    optimized_df[col] = optimized_df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    optimized_df[col] = optimized_df[col].astype(np.int64)  
            elif pd.api.types.is_float_dtype(col_type):
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    optimized_df[col] = optimized_df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    optimized_df[col] = optimized_df[col].astype(np.float32)
                else:
                    optimized_df[col] = optimized_df[col].astype(np.float64)
                    
    final_memory = optimized_df.memory_usage(deep=True).sum() / 1024**2
    
    return optimized_df, initial_memory, final_memory
