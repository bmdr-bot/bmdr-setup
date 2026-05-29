#!/bin/bash
set -euo pipefail

# BMDR Setup - Local Run Script
# Usage: ./scripts/run-local.sh

echo "🚀 Starting BMDR Setup locally..."

cd "$(dirname "$0")/.."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env not found, copying from .env.example"
    cp .env.example .env
fi

# Build and start
docker-compose up --build -d

echo ""
echo "⏳ Waiting for app to start..."
sleep 5

# Health check
if curl -sf http://localhost:8000/health/ > /dev/null 2>&1; then
    echo ""
    echo "✅ App is running!"
    echo ""
    echo "📊 Endpoints:"
    echo "  App:      http://localhost:8000"
    echo "  Docs:     http://localhost:8000/docs"
    echo "  Health:   http://localhost:8000/health/"
    echo "  Ready:    http://localhost:8000/health/ready"
    echo "  Metrics:  http://localhost:8000/health/metrics"
    echo ""
    echo "🛑 Stop: docker-compose down"
else
    echo "❌ App failed to start"
    docker-compose logs app
    exit 1
fi
