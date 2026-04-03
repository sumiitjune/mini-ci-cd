#!/bin/bash

echo "🚀 Deploying app..."

# 🔥 GO TO PROJECT DIRECTORY
cd /app

echo "📂 Current directory:"
pwd

echo "📂 Files here:"
ls

# Pull latest code
git pull origin master

# Rebuild container
docker-compose down
docker-compose up -d --build

echo "✅ Deployment done!"