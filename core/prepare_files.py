import os
import pandas as pd

def process():
    """
    Process and combine datawarrior and GOLD files.
    This is based on 1_preparando_arquivo.py.
    
    Returns:
        pandas.DataFrame: The combined and processed dataframe.
    """
    # Get current directory
    caminho_diretorio = os.getcwd()
    
    # Process actives from DataWarrior
    nome_data = 'actives_datawarrior.txt'
    caminho_data = os.path.join(caminho_diretorio, nome_data)
    df_data = pd.read_csv(caminho_data, delimiter='\t', header=0)
    
    # Remove unwanted columns
    colunas_remover = ['Structure of smiles [idcode]', 'smiles', 'Unnamed: 16']
    df_clean = df_data.drop(columns=colunas_remover, errors='ignore')
    
    # Process decoys from DataWarrior
    nome_dw_decoys = 'decoys_datawarrior.txt'
    caminho_data = os.path.join(caminho_diretorio, nome_dw_decoys)
    df_dw_decoys = pd.read_csv(caminho_data, delimiter='\t', header=0)
    
    # Remove unwanted columns
    df_decoys_clean = df_dw_decoys.drop(columns=colunas_remover, errors='ignore')
    
    # Combine actives and decoys
    df_dw_final = pd.concat([df_clean, df_decoys_clean], axis=0, join='outer')
    df_dw_final = df_dw_final.fillna(0)
    
    # Process actives from GOLD
    nome_gold = 'active_consolidated.csv'
    caminho_arquivo = os.path.join(caminho_diretorio, nome_gold)
    df_cons = pd.read_csv(caminho_arquivo, delimiter=',', header=0)
    df_cons['activity'] = 1
    
    # Process decoys from GOLD
    nome_gold_dec = 'decoys_consolidated.csv'
    caminho_arquivo = os.path.join(caminho_diretorio, nome_gold_dec)
    df_cons_dec = pd.read_csv(caminho_arquivo, delimiter=',', header=0)
    df_cons_dec['activity'] = 0
    
    # Combine GOLD data
    df_gold_final = pd.concat([df_cons, df_cons_dec], axis=0, join='outer')
    df_gold_final = df_gold_final.fillna(0)
    
    # Process DataWarrior name column
    df_dw_final['name'] = df_dw_final['name'].str.replace('Resultados/', '', regex=False)
    df_dw_final['name'] = df_dw_final['name'].str.replace('.pdb', '', regex=False)
    df_dw_final["name"] = df_dw_final.iloc[:,0].str.strip().str.upper()
    
    # Process GOLD name column
    df_gold_final = df_gold_final.rename(columns={'Entry': 'name'})
    df_gold_final['name'] = df_gold_final['name'].str.split('|').str[1]
    df_gold_final['name'] = df_gold_final['name'].str.replace('Resultados/', '', regex=False)
    df_gold_final['name'] = df_gold_final['name'].str.replace('.pdb', '', regex=False)
    df_gold_final["name"] = df_gold_final.iloc[:,0].str.strip().str.upper()
    
    # Combine DataWarrior and GOLD data
    df_concat = pd.concat([df_dw_final, df_gold_final], axis=1)
    
    # Move activity column to the end
    activity_col = df_concat.pop('activity')
    df_concat['activity'] = activity_col
    
    # Check for name discrepancies
    colunas_name_iguais = df_concat['name'].iloc[:, 0] == df_concat['name'].iloc[:, 1]
    
    if colunas_name_iguais.all():
        df_gold_final_sem_primeira_coluna = df_gold_final.iloc[:, 1:]
        df_final = pd.concat([df_dw_final, df_gold_final_sem_primeira_coluna], axis=1)
    else:
        # If there are discrepancies, you can handle them or raise an error
        discrepancias = df_concat[~colunas_name_iguais]
        raise ValueError(f"Name discrepancies found between DataWarrior and GOLD files. First few: {discrepancias.head()}")
    
    # Assign activity
    df_final['atividade'] = activity_col
    
    # Remove unnecessary columns
    remove_colunas = ["Index", "Rescore.Rmsd", "Version"]
    df_final = df_final.drop(columns=remove_colunas, errors='ignore')
    
    # Remove activity column if it exists (we'll keep atividade)
    if 'activity' in df_final.columns:
        df_final.pop('activity')
    
    return df_final 