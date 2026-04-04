#!/bin/bash
set -e

cd /app

echo "🚀 Deploying app..."

git config --global --add safe.directory /app

echo "📥 Pulling latest code..."
git pull origin master

echo "🔁 Restarting container (NO BUILD)..."
docker compose restart

echo "✅ Deployment done!"