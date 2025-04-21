import os
import click
import pandas as pd
import numpy as np
import pickle
import shutil
import warnings
from pathlib import Path
from datetime import datetime

# Suppress sklearn version inconsistency warnings
from sklearn.exceptions import InconsistentVersionWarning
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

@click.group()
def cli():
    """ML Pipeline CLI tool for compound activity prediction."""
    pass

@cli.command('create-model')
@click.option('--actives-datawarrior', 'actives_dw_path', required=True, 
              help='Path to actives_datawarrior.txt file')
@click.option('--decoys-datawarrior', 'decoys_dw_path', required=True,
              help='Path to decoys_datawarrior.txt file')
@click.option('--actives-consolidated', 'actives_cons_path', required=True,
              help='Path to active_consolidated.csv file')
@click.option('--decoys-consolidated', 'decoys_cons_path', required=True,
              help='Path to decoys_consolidated.csv file')
@click.option('--output', 'output_prefix', required=True,
              help='Prefix for output files')
def create_model(actives_dw_path, decoys_dw_path, actives_cons_path, decoys_cons_path, output_prefix):
    """Create ML models from input data files."""
    click.echo(f"Creating models with prefix: {output_prefix}")
    
    # Create temporary directory for processing
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # Copy input files to temp directory
    shutil.copy(actives_dw_path, os.path.join(temp_dir, 'actives_datawarrior.txt'))
    shutil.copy(decoys_dw_path, os.path.join(temp_dir, 'decoys_datawarrior.txt'))
    shutil.copy(actives_cons_path, os.path.join(temp_dir, 'active_consolidated.csv'))
    shutil.copy(decoys_cons_path, os.path.join(temp_dir, 'decoys_consolidated.csv'))
    
    # Change to temp directory
    original_dir = os.getcwd()
    os.chdir(temp_dir)
    
    # Import processing modules
    from core import (
        prepare_files, 
        pre_treatment, 
        normalization, 
        train_models
    )
    
    try:
        # Step 1: Prepare files
        click.echo("Step 1: Preparing files...")
        df_final = prepare_files.process()
        df_final.to_csv('df_final.csv', index=False)
        
        # Step 2: Pre-treatment
        click.echo("Step 2: Pre-treating data...")
        df_var_final = pre_treatment.process('df_final.csv')
        df_var_final.to_csv('df_var_final.csv', index=False)
        
        # Step 3: Normalization
        click.echo("Step 3: Normalizing data...")
        df_reduced, scaler = normalization.process('df_var_final.csv')
        df_reduced.to_csv('df_reduced.csv', index=False)
        
        # Step 4: Train models
        click.echo("Step 4: Training models...")
        models, metrics, data_splits = train_models.process('df_reduced.csv')
        
        # Save outputs with prefix
        models_dir = os.path.join(original_dir, 'models')
        metrics_dir = os.path.join(original_dir, 'metrics')
        data_dir = os.path.join(original_dir, 'data')
        
        # Save models
        for model_name, model in models.items():
            model_path = os.path.join(models_dir, f"{output_prefix}_{model_name}_model.pkl")
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
        
        # Save scaler
        scaler_path = os.path.join(models_dir, f"{output_prefix}_scaler.pkl")
        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler, f)
        
        # Save metrics
        metrics.to_csv(os.path.join(metrics_dir, f"{output_prefix}_metrics.csv"), index=False)
        
        # Save data splits
        np.savez(os.path.join(data_dir, f"{output_prefix}_train_test_data.npz"), 
                 X_train=data_splits['X_train'], 
                 X_test=data_splits['X_test'], 
                 y_train=data_splits['y_train'], 
                 y_test=data_splits['y_test'])
        
        # Save config info
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        config_info = {
            'created_at': timestamp,
            'actives_datawarrior': actives_dw_path,
            'decoys_datawarrior': decoys_dw_path,
            'actives_consolidated': actives_cons_path,
            'decoys_consolidated': decoys_cons_path,
            'output_prefix': output_prefix
        }
        
        config_path = os.path.join(models_dir, f"{output_prefix}_config.pkl")
        with open(config_path, 'wb') as f:
            pickle.dump(config_info, f)
            
        click.echo(f"Model creation completed successfully! Files saved with prefix: {output_prefix}")
        
    except Exception as e:
        click.echo(f"Error during model creation: {str(e)}", err=True)
        raise
    
    finally:
        # Return to original directory and clean up
        os.chdir(original_dir)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

@cli.command('predict')
@click.option('--input-data', required=True, 
              help='Path to data_sem_outliers.csv file')
@click.option('--model-dir', default='models',
              help='Directory containing model files (default: models)')
@click.option('--output', 'output_name', required=True,
              help='Name for output file (without extension)')
def predict(input_data, model_dir, output_name):
    """Predict compound activity using all trained models."""
    click.echo(f"Predicting using models from directory: {model_dir}")
    click.echo(f"Input data: {input_data}")
    
    # Load prediction module
    from core import predict_compounds
    
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(base_dir, model_dir)
        output_dir = os.path.join(base_dir, 'output')
        
        # Run prediction
        click.echo("Running prediction...")
        results = predict_compounds.process_all_models(input_data, models_dir)
        
        # Save results
        output_path = os.path.join(output_dir, f"{output_name}.csv")
        results.to_csv(output_path, index=False)
        
        click.echo(f"Prediction completed successfully! Results saved to: {output_path}")
        
    except Exception as e:
        click.echo(f"Error during prediction: {str(e)}", err=True)
        raise

if __name__ == '__main__':
    cli() 