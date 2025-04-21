# ML Pipeline CLI Tool

(Running with Docker is more simpler)

## Requirements

- Python 3.8 (required)

## Installation

### 1. Install Python 3.8

If you don't have Python 3.8 installed:

#### Ubuntu/Debian:
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.8 python3.8-venv python3.8-dev
```

#### Windows:
Download and install from [python.org](https://www.python.org/downloads/release/python-380/)

#### macOS:
```bash
brew install python@3.8
```

### 2. Create a virtual environment and install dependencies

```bash
# Create a virtual environment
python3.8 -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

## Directory Structure

```
Refactor/
├── cli.py               # Main CLI tool
├── processors/          # Processing modules
│   ├── prepare_files.py
│   ├── pre_treatment.py
│   ├── normalization.py
│   ├── train_models.py
│   └── predict_compounds.py
├── models/              # Saved models
├── metrics/             # Model metrics
├── data/                # Data files
└── output/              # Prediction results
```

## Usage

### Creating Models

To create machine learning models from input data files:

```bash
# Make sure your virtual environment is activated
python cli.py create-model \
  --actives-datawarrior path/to/actives_datawarrior.txt \
  --decoys-datawarrior path/to/decoys_datawarrior.txt \
  --actives-consolidated path/to/active_consolidated.csv \
  --decoys-consolidated path/to/decoys_consolidated.csv \
  --output model_name
```

This will:
1. Process and combine the input files
2. Perform data preprocessing and normalization
3. Train multiple machine learning models
4. Save the models, metrics, and data splits to the appropriate directories with the prefix `model_name`

### Making Predictions

To make predictions on new compounds:

```bash
# Make sure your virtual environment is activated
python cli.py predict \
  --input-data path/to/data_sem_outliers.csv \
  --output results_name
```

This will:
1. Load all available models from the models directory
2. Make predictions on the input data
3. Create a consensus prediction based on all models
4. Save the results to `output/results_name.csv`

You can also specify a custom models directory:

```bash
python cli.py predict \
  --input-data path/to/data_sem_outliers.csv \
  --model-dir custom/models/path \
  --output results_name
```

## Input File Formats

### For Model Creation

- **actives_datawarrior.txt**: Tab-separated file with active compounds from DataWarrior
- **decoys_datawarrior.txt**: Tab-separated file with decoy compounds from DataWarrior
- **active_consolidated.csv**: Comma-separated file with active compounds from GOLD
- **decoys_consolidated.csv**: Comma-separated file with decoy compounds from GOLD

### For Prediction

- **data_sem_outliers.csv**: Comma-separated file with compounds to predict
  - Should have the same feature columns as used in training
  - Should have a 'NAME' column with compound identifiers

## Output Files

### Model Creation

- `models/{prefix}_LR_model.pkl`: Logistic Regression model
- `models/{prefix}_NB_model.pkl`: Naive Bayes model
- `models/{prefix}_DT_model.pkl`: Decision Tree model
- `models/{prefix}_RF_model.pkl`: Random Forest model
- `models/{prefix}_SVM_model.pkl`: Support Vector Machine model
- `models/{prefix}_XGB_model.pkl`: XGBoost model
- `models/{prefix}_scaler.pkl`: MinMaxScaler used for normalization
- `models/{prefix}_config.pkl`: Configuration information
- `metrics/{prefix}_metrics.csv`: Model performance metrics
- `data/{prefix}_train_test_data.npz`: Training and test data splits

### Prediction

- `output/{output_name}.csv`: Prediction results with consensus 