#!/usr/bin/env sh

# Define PYTHONPATH
cd "$(dirname "$0")"
PYTHONPATH=".."
ls "$PYTHONPATH"
export PYTHONPATH

# Run unit tests
RUN_UNIT=true
if ${RUN_UNIT}; then
    printf "INFO: Running unit tests ...\n"
    pytest unit_tests/
fi
