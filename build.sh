#!/usr/bin/env bash

echo "▶️ Using runtime.txt to set Python version..."
python --version

# Install dependencies
pip install -r requirements-github.txt
