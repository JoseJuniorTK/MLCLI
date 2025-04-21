# Configuração Docker para Ferramenta CLI de Pipeline de ML

Este guia explica como executar a Ferramenta CLI de Pipeline de ML usando Docker.

## Pré-requisitos

- Docker instalado em seu sistema (https://docs.docker.com/engine/install/ubuntu/)
- Docker Compose instalado em seu sistema (https://docs.docker.com/compose/install/linux/#install-using-the-repository)

## Primeiros Passos

1. Clone o repositório e navegue até o diretório do projeto:

2. Construa e inicie o container Docker:

```bash
docker compose build
docker compose up -d
```

## Executando os Workflows

Execute os comandos diretamente com a sintaxe simplificada:

```bash
# Create model
docker compose exec mlcli create-model \
  --actives-datawarrior example_files/actives_datawarrior.txt \
  --decoys-datawarrior example_files/decoys_datawarrior.txt \
  --actives-consolidated example_files/active_consolidated.csv \
  --decoys-consolidated example_files/decoys_consolidated.csv \
  --output prefixo_da_saida

# Predict
docker compose exec mlcli predict \
  --input-data example_files/data_sem_outliers.csv \
  --output nome_saida
```

Você também pode especificar um diretório de modelos personalizado:

```bash
docker compose exec mlcli predict \
  --input-data example_files/data_sem_outliers.csv \
  --model-dir caminho/personalizado/modelos \
  --output nome_saida
```

## Parando o Container

Quando terminar, você pode parar o container:

```bash
docker compose down
```

## Localização dos Arquivos

O container Docker monta o diretório do projeto em `/app` dentro do container. Todos os arquivos gerados durante os workflows estarão disponíveis em seus respectivos diretórios na sua máquina host:

- Modelos: `./models/`
- Métricas: `./metrics/`
- Saída: `./output/`
- Dados: `./data/`

## Dados de Exemplo

Arquivos de dados de exemplo estão disponíveis no diretório `example_files/`. Você pode usar estes para testar os workflows. 

## Compatibilidade de Versões

Este projeto utiliza scikit-learn versão 1.3.2. Avisos de incompatibilidade de versão ao carregar modelos serão automaticamente suprimidos pelo código. Se você precisar usar modelos treinados com outras versões do scikit-learn, pode ser necessário retreinar os modelos com a versão atual. 