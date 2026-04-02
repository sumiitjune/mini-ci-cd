#!/bin/sh

echo "🚀 Deploying app..."

pwd
ls

echo "📥 Pulling latest code..."
git pull origin main

echo "🐳 Restarting containers..."
docker compose down
docker compose up --build -d

echo "✅ Deployment done!"