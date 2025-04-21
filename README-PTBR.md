# Ferramenta de Linha de Comando para Pipeline de ML

(Rodar com o Docker é mais simples)

## Requisitos

- Python 3.8 (preferencial)

## Instalação

### 1. Instalar Python 3.8

Se você não tem o Python 3.8 instalado:

#### Ubuntu/Debian:
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.8 python3.8-venv python3.8-dev
```

#### Windows:
Baixe e instale a partir de [python.org](https://www.python.org/downloads/release/python-380/)

#### macOS:
```bash
brew install python@3.8
```

### 2. Criar um ambiente virtual e instalar dependências

```bash
# Criar ambiente virtual
python3.8 -m venv venv

# Ativar o ambiente virtual
# No Linux/macOS:
source venv/bin/activate
# No Windows:
# venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
pip install -e .
```

## Estrutura de Diretórios

```
Refactor/
├── cli.py               # Ferramenta principal de linha de comando
├── processors/          # Módulos de processamento
│   ├── prepare_files.py
│   ├── pre_treatment.py
│   ├── normalization.py
│   ├── train_models.py
│   └── predict_compounds.py
├── models/              # Modelos salvos
├── metrics/             # Métricas dos modelos
├── data/                # Arquivos de dados
└── output/              # Resultados das predições
```

## Uso

### Criando Modelos

Para criar modelos de aprendizado de máquina a partir de arquivos de dados de entrada:

```bash
# Certifique-se de que seu ambiente virtual está ativado
python cli.py create-model \
  --actives-datawarrior path/to/actives_datawarrior.txt \
  --decoys-datawarrior path/to/decoys_datawarrior.txt \
  --actives-consolidated path/to/active_consolidated.csv \
  --decoys-consolidated path/to/decoys_consolidated.csv \
  --output model_name
```

Isso irá:
1. Processar e combinar os arquivos de entrada
2. Realizar pré-processamento e normalização dos dados
3. Treinar múltiplos modelos de aprendizado de máquina
4. Salvar os modelos, métricas e divisões de dados nos diretórios apropriados com o prefixo `model_name`

### Fazendo Predições

Para fazer predições em novos compostos:

```bash
# Certifique-se de que seu ambiente virtual está ativado
python cli.py predict \
  --input-data path/to/data_sem_outliers.csv \
  --model-prefix model_name \
  --output results_name
```

Isso irá:
1. Carregar os modelos com o prefixo especificado
2. Fazer predições nos dados de entrada
3. Criar uma predição de consenso baseada em todos os modelos
4. Salvar os resultados em `output/results_name.csv`

## Formatos dos Arquivos de Entrada

### Para Criação de Modelos

- **actives_datawarrior.txt**: Arquivo separado por tabulação com compostos ativos do DataWarrior
- **decoys_datawarrior.txt**: Arquivo separado por tabulação com compostos decoy do DataWarrior
- **active_consolidated.csv**: Arquivo separado por vírgula com compostos ativos do GOLD
- **decoys_consolidated.csv**: Arquivo separado por vírgula com compostos decoy do GOLD

### Para Predição

- **data_sem_outliers.csv**: Arquivo separado por vírgula com compostos para predição
  - Deve ter as mesmas colunas de características usadas no treinamento
  - Deve ter uma coluna 'NAME' com identificadores de compostos

## Arquivos de Saída

### Criação de Modelos

- `models/{prefix}_LR_model.pkl`: Modelo de Regressão Logística
- `models/{prefix}_NB_model.pkl`: Modelo de Naive Bayes
- `models/{prefix}_DT_model.pkl`: Modelo de Árvore de Decisão
- `models/{prefix}_RF_model.pkl`: Modelo de Floresta Aleatória
- `models/{prefix}_SVM_model.pkl`: Modelo de Máquina de Vetores de Suporte
- `models/{prefix}_XGB_model.pkl`: Modelo XGBoost
- `models/{prefix}_scaler.pkl`: MinMaxScaler usado para normalização
- `models/{prefix}_config.pkl`: Informações de configuração
- `metrics/{prefix}_metrics.csv`: Métricas de desempenho dos modelos
- `data/{prefix}_train_test_data.npz`: Divisões de dados de treino e teste

### Predição

- `output/{output_name}.csv`: Resultados das predições com consenso 