#!/bin/bash

CACHE_DIR="/Volumes/config/custom_components/hitron/__pycache__"

if [ -d "$CACHE_DIR" ]; then
    echo "Deleting $CACHE_DIR..."
    rm -rf "$CACHE_DIR"
    echo "Done."
else
    echo "No __pycache__ directory found at $CACHE_DIR."
fi