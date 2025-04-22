# Docker Setup for ML Pipeline CLI Tool

This guide explains how to run the ML Pipeline CLI Tool using Docker.

## Prerequisites

- Docker installed on your system (https://docs.docker.com/engine/install/ubuntu/ and https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)
- Docker Compose installed on your system (https://docs.docker.com/compose/install/linux/#install-using-the-repository)

## Getting Started

1. Clone the repository and navigate to the project directory:

2. Build and start the Docker container:

```bash
docker compose build
docker compose up -d
```

## Running the Workflows

### Option 1: Using the helper script (Recommended)

A helper script `ml-cli.sh` is provided for simplified usage:

```bash
# Make the script executable (first time only)
chmod +x ml-cli.sh

# Get help
./ml-cli.sh --help

# Create model
./ml-cli.sh create-model \
  --actives-datawarrior example_files/actives_datawarrior.txt \
  --decoys-datawarrior example_files/decoys_datawarrior.txt \
  --actives-consolidated example_files/active_consolidated.csv \
  --decoys-consolidated example_files/decoys_consolidated.csv \
  --output model_name

# Predict
./ml-cli.sh predict \
  --input-data example_files/data_sem_outliers.csv \
  --output output_name
```

The script will automatically start the container if it's not running.

### Option 2: Using Docker Compose directly

Run the commands with Docker Compose:

```bash
# Create model
docker compose exec mlcli python cli.py create-model \
  --actives-datawarrior example_files/actives_datawarrior.txt \
  --decoys-datawarrior example_files/decoys_datawarrior.txt \
  --actives-consolidated example_files/active_consolidated.csv \
  --decoys-consolidated example_files/decoys_consolidated.csv \
  --output model_name

# Predict
docker compose exec mlcli python cli.py predict \
  --input-data example_files/data_sem_outliers.csv \
  --output output_name
```

You can also specify a custom models directory:

```bash
./ml-cli.sh predict \
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