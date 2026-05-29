#!/bin/bash
set -euo pipefail

# BMDR Setup - Build Script
# Usage: ./scripts/build.sh [tag]

TAG="${1:-latest}"
APP_NAME="${APP_NAME:-bmdr-setup}"

echo "🔨 Building $APP_NAME:$TAG..."

cd "$(dirname "$0")/.."

# Build with BuildKit if available
if docker buildx version > /dev/null 2>&1; then
    echo "📦 Using BuildKit..."
    docker buildx build \
        --platform linux/amd64 \
        -t "$APP_NAME:$TAG" \
        -t "$APP_NAME:latest" \
        --load \
        .
else
    echo "📦 Using legacy builder..."
    docker build -t "$APP_NAME:$TAG" -t "$APP_NAME:latest" .
fi

echo "✅ Built $APP_NAME:$TAG"
echo ""
echo "Run locally:"
echo "  docker run -p 8000:8000 $APP_NAME:$TAG"
