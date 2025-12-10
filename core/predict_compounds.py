import os
import pandas as pd
import pickle
import re
import warnings
from sklearn.exceptions import InconsistentVersionWarning


def process_all_models(input_file, models_dir):
    """
    Make predictions using all available trained models in the models directory.

    Args:
        input_file (str): Path to the input CSV file with compounds to predict.
        models_dir (str): Directory containing model files.

    Returns:
        pandas.DataFrame: DataFrame with prediction results and consensus.
    """
    loaded_models = {}
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.pkl')]

    if not model_files:
        raise ValueError(f"No model files found in {models_dir}")

    for model_file in model_files:
        model_path = os.path.join(models_dir, model_file)
        try:
            match = re.search(r'_(LR|NB|DT|RF|SVM|XGB)_', model_file)
            if not match:
                continue

            model_type = match.group(1)
            if model_type in loaded_models:
                continue

            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
                with open(model_path, 'rb') as file:
                    loaded_object = pickle.load(file)
                    if hasattr(loaded_object, 'predict_proba') and callable(getattr(loaded_object, 'predict_proba')):
                        loaded_models[model_type] = loaded_object
                        print(f"Loaded model: {model_type} from {model_file}")
        except Exception as e:
            print(f"Error loading {model_file}: {str(e)}")

    if not loaded_models:
        raise ValueError(f"No valid models found in {models_dir}")

    print(f"Loaded {len(loaded_models)} models: {', '.join(loaded_models.keys())}")

    return _process_with_models(input_file, loaded_models)

def _process_with_models(input_file, loaded_models):
    """
    Common processing function used by both process and process_all_models.
    
    Args:
        input_file (str): Path to the input CSV file with compounds to predict.
        loaded_models (dict): Dictionary of loaded model objects.
    
    Returns:
        pandas.DataFrame: DataFrame with prediction results and consensus.
    """
    # Load data
    new_compounds = pd.read_csv(input_file, delimiter=',')
    
    # Extract NAME column
    if 'NAME' in new_compounds.columns:
        df_name = new_compounds['NAME']
    elif 'name' in new_compounds.columns:
        df_name = new_compounds['name']
    else:
        # If no name column exists, create a default one
        df_name = pd.Series([f"Compound_{i}" for i in range(len(new_compounds))])
    
    # Check for required columns
    model_ref = next(iter(loaded_models.values()))  # Get first model to check features
    expected_columns = model_ref.feature_names_in_
    
    # Process input data if needed
    for col in expected_columns:
        if col not in new_compounds.columns:
            raise ValueError(f"Required column '{col}' not found in input data")
    
    # Ensure columns match model expectations
    input_features = new_compounds[expected_columns]
    
    # Make predictions with all models
    for model_name, model in loaded_models.items():
        # Calculate probability of being active
        prob_active = model.predict_proba(input_features)[:, 1]
        # Add predictions as a new column
        new_compounds[f'ativd_pred_{model_name}'] = prob_active
    
    # Find prediction columns
    pred_columns = [col for col in new_compounds.columns if col.startswith('ativd_pred_')]
    
    # Create consensus column (count of models predicting active)
    new_compounds['consensus'] = (new_compounds[pred_columns] > 0.5).sum(axis=1)
    
    # Create consensus_Model column (list of models predicting active)
    def models_above_05(row):
        models = [col.replace('ativd_pred_', '') for col in pred_columns if row[col] > 0.5]
        return ', '.join(models)
    
    new_compounds['consensus_Model'] = new_compounds.apply(models_above_05, axis=1)
    
    # Prepare final output
    df_name = pd.DataFrame(df_name)
    
    # Create output with NAME column, predictions, and consensus
    df_pred = df_name.copy()
    for col in pred_columns + ['consensus', 'consensus_Model']:
        df_pred[col] = new_compounds[col]
    
    return df_pred 