import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def process(input_file):
    """
    Normalize data and remove correlated features.
    This is based on 3_tratamento_normaliz.py.
    
    Args:
        input_file (str): Path to the input CSV file.
    
    Returns:
        tuple: (processed_df, scaler)
            - processed_df: The normalized and reduced dataframe.
            - scaler: The fitted MinMaxScaler for future use.
    """
    # Load the dataframe
    df = pd.read_csv(input_file, delimiter=',')
    
    # Extract name and activity columns
    df_name = df.pop('name')
    df_atividade = df.pop('atividade')
    
    # Initialize the MinMaxScaler
    scaler = MinMaxScaler()
    
    # Normalize the DataFrame
    df_normalizado = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
    
    # Calculate correlation matrix
    cor_matrix = df_normalizado.corr()
    
    # Remove highly correlated columns (correlation > 0.5)
    corte = 0.5
    to_drop = set()
    for i in range(len(cor_matrix.columns)):
        for j in range(i):
            if abs(cor_matrix.iloc[i, j]) > corte:
                colname = cor_matrix.columns[i]
                to_drop.add(colname)
    
    # Create reduced dataframe
    df_reduced = df_normalizado.drop(columns=to_drop)
    
    # Add back the activity column
    df_reduced.loc[:, 'atividade'] = df_atividade

    return df_reduced, scaler 