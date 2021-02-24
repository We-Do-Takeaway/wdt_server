#!/bin/sh
CONTAINER_ALREADY_STARTED="/home/vscode/CONTAINER_ALREADY_STARTED_PLACEHOLDER"

if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
    pwd
    echo $PATH
    touch $CONTAINER_ALREADY_STARTED
    echo "-- First container startup --"

    cd /workspace
    poetry install
    pre-commit install
fi

sleep infinity
