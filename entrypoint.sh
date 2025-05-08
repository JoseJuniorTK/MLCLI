#!/usr/bin/env bash
set -e

# If no arguments are passed, just keep the container alive
if [ "$#" -eq 0 ]; then
    exec tail -f /dev/null
else
    # Otherwise, run the CLI with passed arguments
    exec python /app/cli.py "$@"
fi
