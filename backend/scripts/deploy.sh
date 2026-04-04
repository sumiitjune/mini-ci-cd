#!/bin/bash
set -e

cd /app

echo "🚀 Deploying app..."

git config --global --add safe.directory /app

echo "📥 Pulling latest code..."
git pull origin master

echo "🛑 Stopping old containers..."
docker compose down

echo "🐳 Rebuilding containers..."
docker compose up -d --build

echo "✅ Deployment done!"