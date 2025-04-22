#!/bin/bash
set -e

# If no arguments are provided or the command is the default tail -f /dev/null, 
# just keep the container running
if [ "$#" -eq 0 ] || [ "$1" = "tail" -a "$2" = "-f" -a "$3" = "/dev/null" ]; then
    exec tail -f /dev/null
else
    # Otherwise, execute the cli.py script with all arguments
    exec python /app/cli.py "$@"
fi 