import os
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
    
    # For preserving columns of interest as described in the original script
    # This part would normally save minmax_scaler_interest.pkl but we'll return the scaler instead
    columns_of_interest = [
        'Total Molweight', 'cLogP', 'H-Acceptors', 'H-Donors',
        'Druglikeness', 'Molecular Flexibility',
        'PLP.Chemscore.Hbond', 'PLP.part.buried', 'PLP.part.repulsive',
        'energies_residues.GLN198.PLP.S(buried)', 'energies_residues.GLN198.PLP.total',
        'energies_residues.GLU263.PLP.S(buried)', 'energies_residues.GLU263.PLP.total',
        'energies_residues.ILE365.PLP.total',
        'energies_residues.MET261.PLP.S(buried)', 'energies_residues.MET261.PLP.S(nonpolar)',
        'energies_residues.PHE367.PLP.S(buried)', 'energies_residues.TYR260.PLP.total',
        'energies_residues.TYR366.PLP.S(buried)', 'energies_residues.ARG263.PLP.S(buried)',
        'energies_residues.ASP264.PLP.S(buried)', 'energies_residues.ILE265.PLP.S(buried)',
        'energies_residues.PHE51.PLP.S(buried)'
    ]
    
    # Filter columns of interest that are actually in the dataframe
    available_columns = [col for col in columns_of_interest if col in df.columns]
    
    # Save scaler for columns of interest if they exist in the data
    if available_columns:
        special_scaler = MinMaxScaler()
        df_subset = df[available_columns]
        special_scaler.fit(df_subset)
    
    return df_reduced, scaler 