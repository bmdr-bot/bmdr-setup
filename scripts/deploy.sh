#!/bin/bash
set -euo pipefail

# BMDR Setup - Deployment Script
# Usage: ./deploy.sh [environment]

ENVIRONMENT="${1:-staging}"
APP_NAME="${APP_NAME:-bmdr-app}"
COMPOSE_FILE="docker-compose.prod.yml"

echo "🚀 Deploying $APP_NAME to $ENVIRONMENT..."

# Check prerequisites
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found"
    exit 1
fi

# Load environment variables
if [ -f ".env.$ENVIRONMENT" ]; then
    echo "📋 Loading .env.$ENVIRONMENT"
    export $(grep -v '^#' .env.$ENVIRONMENT | xargs)
elif [ -f ".env" ]; then
    echo "📋 Loading .env"
    export $(grep -v '^#' .env | xargs)
fi

# Validate required variables
if [ -z "${CF_TUNNEL_TOKEN:-}" ]; then
    echo "⚠️  CF_TUNNEL_TOKEN not set - tunnel won't start"
fi

# Pull latest images
echo "📥 Pulling latest images..."
docker-compose -f $COMPOSE_FILE pull

# Deploy
echo "🟢 Starting services..."
docker-compose -f $COMPOSE_FILE up -d

# Wait for health check
echo "⏳ Waiting for health check..."
sleep 5

if curl -sf http://localhost:8000/health/ > /dev/null 2>&1; then
    echo "✅ Deployment successful!"
    echo ""
    echo "📊 Status:"
    docker-compose -f $COMPOSE_FILE ps
    echo ""
    echo "🌐 Health: http://localhost:8000/health/"
else
    echo "❌ Health check failed"
    echo "📋 Logs:"
    docker-compose -f $COMPOSE_FILE logs --tail=50 app
    exit 1
fi
