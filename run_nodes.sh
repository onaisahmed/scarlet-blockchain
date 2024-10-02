#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

export PYTHONPATH=$(pwd)  # Set PYTHONPATH to the current directory

echo "Starting Node 1 on port 5001..."
python nodes/node1.py &  # Run node1 in the background
echo "Starting Node 2 on port 5002..."
python nodes/node2.py &  # Run node2 in the background
echo "Starting Node 3 on port 5003..."
python nodes/node3.py &  # Run node3 in the background

wait  # Wait for all background processes to complete
