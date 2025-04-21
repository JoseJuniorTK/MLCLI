import os
import pandas as pd

def process(input_file):
    """
    Preprocess dataframe by removing columns with many zeros and low variance.
    This is based on 2_pre_tratamento.py.
    
    Args:
        input_file (str): Path to the input CSV file.
        
    Returns:
        pandas.DataFrame: The processed dataframe.
    """
    # Load the dataframe
    df = pd.read_csv(input_file, delimiter=',')
    
    # Extract name and activity columns
    df_name = df.pop('name')
    df_atividade = df.pop('atividade')
    
    # Convert all remaining columns to numeric
    df = df.apply(pd.to_numeric, errors='coerce')
    
    # Fill any NaN values with 0
    df = df.fillna(0)
    
    # Remove columns with more than 50% zeros
    threshold = len(df) * 0.5
    df_filtered = df.loc[:, (df == 0).sum(axis=0) <= threshold]
    
    # Remove columns with low variance
    variances = df_filtered.var()
    variance_threshold = 0.01
    columns_to_keep = variances[variances >= variance_threshold].index
    df_var = df_filtered[columns_to_keep]
    
    # Add back the name and activity columns
    df_var.insert(0, 'name', df_name)
    df_var.loc[:, 'atividade'] = df_atividade
    
    return df_var 