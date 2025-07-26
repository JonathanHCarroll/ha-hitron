#!/bin/bash

set -e

# Define paths
SRC="/Users/jonathan/Dev/HA/ha-hitron"
DST="/Volumes/config/custom_components/hitron"

# Safety check: Ensure target is mounted
if [ ! -d "/Volumes/config" ]; then
  echo "❌ Target volume /Volumes/config is not mounted. Please mount the SMB share first."
  exit 1
fi

echo "🚀 Deploying from $SRC to $DST"

# Optional: Remove __pycache__ folders from destination
echo "🧹 Cleaning up old __pycache__ directories..."
find "$DST" -type d -name "__pycache__" -exec rm -rf {} +

# Sync files (excluding hidden files and .pyc)
rsync -av --inplace --delete \
  --exclude=".git/" \
  --exclude=".venv/" \
  --exclude=".*" \
  --exclude="__pycache__/" \
  --exclude="*.pyc" \
  "$SRC/" "$DST/"
  
echo "✅ Deployment complete!"