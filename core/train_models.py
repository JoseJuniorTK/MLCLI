import os
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score,
    matthews_corrcoef, cohen_kappa_score, accuracy_score
)
from imblearn.over_sampling import SMOTE

def process(input_file):
    """
    Train and evaluate multiple ML models on the processed data.
    This is based on 4_smote_ml_v2.py.
    
    Args:
        input_file (str): Path to the input CSV file.
    
    Returns:
        tuple: (models, metrics_df, data_splits)
            - models: Dictionary of trained models
            - metrics_df: DataFrame of model performance metrics
            - data_splits: Dictionary containing X_train, X_test, y_train, y_test
    """
    # Load the dataframe
    df = pd.read_csv(input_file, delimiter=',')
    
    # Separate features and target
    X = df.drop('atividade', axis=1)
    y = df['atividade']
    
    # Apply SMOTE to balance classes
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)
    
    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.2, random_state=42
    )
    
    # Define models and their parameters for optimization
    models_params = {
        'LR': (LogisticRegression(), {'C': [0.1, 1, 10]}),
        'NB': (GaussianNB(), {'var_smoothing': [1e-2, 1e-5, 1e-9, 1e-15]}),
        'DT': (DecisionTreeClassifier(), {'max_depth': [3, 5, 10], 'min_samples_split': [2, 5, 10]}),
        'RF': (RandomForestClassifier(), {'n_estimators': [50, 100, 200], 'max_depth': [None, 10, 20]}),
        'SVM': (SVC(probability=True), {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf']}),
        'XGB': (XGBClassifier(eval_metric='logloss'), {'n_estimators': [50, 100, 200], 'learning_rate': [0.01, 0.1, 0.2]})
    }
    
    # K-Fold Cross Validation
    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    best_models = {}
    scores = {}
    
    # Train models
    for name, (model, params) in models_params.items():
        grid_search = GridSearchCV(model, params, cv=kfold, scoring='accuracy')
        grid_search.fit(X_train, y_train)
        best_models[name] = grid_search.best_estimator_
        best_score = grid_search.best_score_
        scores[name] = best_score
    
    # Create results DataFrame
    results_df = pd.DataFrame({
        'Model': list(models_params.keys()),
        'Best Model': [str(best_models[name]) for name in best_models.keys()],
        'Accuracy': [scores[name] for name in scores.keys()]
    })
    
    # Dictionary for metrics
    metrics_dict = {
        'Modelo': [],
        'Banco': [],
        'Revocação': [],
        'Precisão': [],
        'Sensibilidade': [],
        'Especificidade': [],
        'Acurácia': [],
        'Erro': [],
        'Medida F': [],
        'Kappa de Cohen': [],
        'MCC': [],
        'AUC ROC': []
    }
    
    # Evaluate models
    for name, model in best_models.items():
        y_pred_train = model.predict(X_train)
        y_prob_train = model.predict_proba(X_train)[:,1]
        
        y_pred_test = model.predict(X_test)
        y_prob_test = model.predict_proba(X_test)[:,1]
        
        for (y_true, y_pred, y_prob, banco) in [
            (y_train, y_pred_train, y_prob_train, "Treinamento"), 
            (y_test, y_pred_test, y_prob_test, "Teste")
        ]:
            cm = confusion_matrix(y_true, y_pred)
            
            acc = (cm[0,0] + cm[1,1]) / sum(sum(cm))
            err = 1 - acc
            sensitivity = cm[1,1] / (cm[1,0] + cm[1,1]) if (cm[1,0] + cm[1,1]) > 0 else 0
            specificity = cm[0,0] / (cm[0,0] + cm[0,1]) if (cm[0,0] + cm[0,1]) > 0 else 0
            f1 = 2 * ((sensitivity * specificity) / (sensitivity + specificity)) if (sensitivity + specificity) > 0 else 0
            auc = roc_auc_score(y_true, y_prob)
            mcc = matthews_corrcoef(y_true, y_pred)
            kappa = cohen_kappa_score(y_true, y_pred)
            
            precision = cm[1,1] / (cm[1,1] + cm[0,1]) if (cm[1,1] + cm[0,1]) > 0 else 0
            
            # Store metrics
            metrics_dict['Modelo'].append(name)
            metrics_dict['Banco'].append(banco)
            metrics_dict['Revocação'].append(round(sensitivity * 100, 2))
            metrics_dict['Precisão'].append(round(precision * 100, 2))
            metrics_dict['Sensibilidade'].append(round(sensitivity * 100, 2))
            metrics_dict['Especificidade'].append(round(specificity * 100, 2))
            metrics_dict['Acurácia'].append(round(acc * 100, 2))
            metrics_dict['Erro'].append(round(err * 100, 2))
            metrics_dict['Medida F'].append(round(f1, 2))
            metrics_dict['Kappa de Cohen'].append(round(kappa, 2))
            metrics_dict['MCC'].append(round(mcc, 2))
            metrics_dict['AUC ROC'].append(round(auc, 2))
    
    # Convert metrics to DataFrame
    metrics_df = pd.DataFrame(metrics_dict)
    
    # Prepare return values
    data_splits = {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test
    }
    
    return best_models, metrics_df, data_splits 