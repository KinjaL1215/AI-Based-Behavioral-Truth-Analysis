#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Install Ubuntu system dependencies for MediaPipe/OpenCV
apt-get update && apt-get install -y libgl1 libgles2 libglib2.0-0
