# Configuração Docker para Ferramenta CLI de Pipeline de ML

Este guia explica como executar a Ferramenta CLI de Pipeline de ML usando Docker.

## Pré-requisitos

- Docker instalado em seu sistema (https://docs.docker.com/engine/install/ubuntu/ e https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)
- Docker Compose instalado em seu sistema (https://docs.docker.com/compose/install/linux/#install-using-the-repository)

## Primeiros Passos

1. Clone o repositório e navegue até o diretório do projeto:

2. Construa e inicie o container Docker:

```bash
docker compose build
docker compose up -d
```

## Executando os Workflows

### Opção 1: Usando o script auxiliar (Recomendado)

Um script auxiliar `ml-cli.sh` é fornecido para uso simplificado:

```bash
# Torne o script executável (apenas na primeira vez)
chmod +x ml-cli.sh

# Obter ajuda
./ml-cli.sh --help

# Criar modelo
./ml-cli.sh create-model \
  --actives-datawarrior example_files/actives_datawarrior.txt \
  --decoys-datawarrior example_files/decoys_datawarrior.txt \
  --actives-consolidated example_files/active_consolidated.csv \
  --decoys-consolidated example_files/decoys_consolidated.csv \
  --output prefixo_da_saida

# Prever
./ml-cli.sh predict \
  --input-data example_files/data_sem_outliers.csv \
  --output nome_saida
```

O script iniciará automaticamente o contêiner se ele não estiver em execução.

### Opção 2: Usando o Docker Compose diretamente

Execute os comandos com o Docker Compose:

```bash
# Criar modelo
docker compose exec mlcli python cli.py create-model \
  --actives-datawarrior example_files/actives_datawarrior.txt \
  --decoys-datawarrior example_files/decoys_datawarrior.txt \
  --actives-consolidated example_files/active_consolidated.csv \
  --decoys-consolidated example_files/decoys_consolidated.csv \
  --output prefixo_da_saida

# Prever
docker compose exec mlcli python cli.py predict \
  --input-data example_files/data_sem_outliers.csv \
  --output nome_saida
```

Você também pode especificar um diretório de modelos personalizado:

```bash
./ml-cli.sh predict \
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