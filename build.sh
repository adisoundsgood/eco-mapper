#!/bin/bash

# Exit on error
set -e

# Build React app
cd frontend
npm install
npm run build
cd ..

# Move build files to Flask directories
python move_build.py

echo "Build process completed successfully."