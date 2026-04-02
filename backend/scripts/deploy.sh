#!/bin/sh

echo "🚀 Deploying app..."

cd /app

git pull origin main

docker compose down
docker compose up --build -d

echo "✅ Deployment done!"
