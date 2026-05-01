#!/bin/bash
# Start the background monitor in the background
python monitor.py &

# Start the Flask app
python app.py
