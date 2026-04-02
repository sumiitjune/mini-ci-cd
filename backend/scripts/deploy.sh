#!/bin/sh

echo "🚀 Deploying app..."

cd /app

echo "📂 Checking files..."
ls

echo "🐳 Rebuilding containers..."
docker-compose down
docker-compose up --build -d

echo "✅ Deployment done!"