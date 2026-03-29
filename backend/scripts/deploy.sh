#!/bin/bash

echo "🚀 Deploying app..."

docker stop my-app || true
docker rm my-app || true

docker build -t my-app ../backend
docker run -d -p 5000:5000 --name my-app my-app

echo "✅ Deployment done!"
