#!/bin/bash

echo " Starting deployment..."

cd /app

git pull origin master

echo " Building Docker image..."
docker build -t my-app .

echo " Stopping old container..."
docker stop my-container || true
docker rm my-container || true

echo " Starting new container..."
docker run -d -p 3000:3000 --name my-container my-app

echo " Deployment complete!"#!/bin/bash

echo " Deploying app..."

docker stop my-app || true
docker rm my-app || true

docker build -t my-app ../backend
docker run -d -p 5000:5000 --name my-app my-app

echo " Deployment done!"
