# Docker Setup for ML Pipeline CLI Tool

This guide explains how to run the ML Pipeline CLI Tool using Docker.

## Prerequisites

- Docker installed on your system (https://docs.docker.com/engine/install/ubuntu/)
- Docker Compose installed on your system (https://docs.docker.com/compose/install/linux/#install-using-the-repository)

## Getting Started

1. Clone the repository and navigate to the project directory:

2. Build and start the Docker container:

```bash
docker compose build
docker compose up -d
```

## Running the Workflows

Run the commands directly with the simplified syntax:

```bash
# Create model
docker compose exec mlcli create-model \
  --actives-datawarrior example_files/actives_datawarrior.txt \
  --decoys-datawarrior example_files/decoys_datawarrior.txt \
  --actives-consolidated example_files/active_consolidated.csv \
  --decoys-consolidated example_files/decoys_consolidated.csv \
  --output model_name

# Predict
docker compose exec mlcli predict \
  --input-data example_files/data_sem_outliers.csv \
  --output output_name
```

You can also specify a custom models directory:

```bash
docker compose exec mlcli predict \
  --input-data example_files/data_sem_outliers.csv \
  --model-dir custom/models/path \
  --output output_name
```

## Stopping the Container

When you're done, you can stop the container:

```bash
docker compose down
```

## File Locations

The Docker container mounts the project directory to `/app` in the container. All files generated during the workflows will be available in their respective directories on your host machine:

- Models: `./models/`
- Metrics: `./metrics/`
- Output: `./output/`
- Data: `./data/`

## Sample Data

Sample data files are available in the `example_files/` directory. You can use these to test the workflows. 

## Version Compatibility

This project uses scikit-learn version 1.3.2. Version incompatibility warnings when loading models will be automatically suppressed by the code. If you need to use models trained with other versions of scikit-learn, you may need to retrain the models with the current version. 