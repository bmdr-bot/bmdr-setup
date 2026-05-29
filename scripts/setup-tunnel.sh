#!/bin/bash
set -euo pipefail

# BMDR Setup - Cloudflare Tunnel Setup
# Usage: ./setup-tunnel.sh <tunnel-name>

TUNNEL_NAME="${1:-bmdr-app}"

echo "🌐 Setting up Cloudflare Tunnel: $TUNNEL_NAME"

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo "📥 Installing cloudflared..."
    
    # Detect architecture
    ARCH=$(uname -m)
    case $ARCH in
        x86_64) CLOUDFLARED_ARCH="amd64" ;;
        aarch64) CLOUDFLARED_ARCH="arm64" ;;
        *) echo "❌ Unsupported architecture: $ARCH"; exit 1 ;;
    esac
    
    # Download and install
    curl -L --output cloudflared.deb "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-${CLOUDFLARED_ARCH}.deb"
    sudo dpkg -i cloudflared.deb || sudo apt-get install -f -y
    rm cloudflared.deb
fi

# Login (opens browser)
echo "🔑 Authenticating with Cloudflare..."
cloudflared tunnel login

# Create tunnel
echo "🚇 Creating tunnel..."
TUNNEL_ID=$(cloudflared tunnel create "$TUNNEL_NAME" | grep -oP 'Created tunnel \K[a-z0-9-]+' || true)

if [ -z "$TUNNEL_ID" ]; then
    echo "⚠️  Tunnel may already exist. Getting existing tunnel ID..."
    TUNNEL_ID=$(cloudflared tunnel list | grep "$TUNNEL_NAME" | awk '{print $1}' | head -1)
fi

echo "✅ Tunnel ID: $TUNNEL_ID"

# Get credentials file path
CREDENTIALS_FILE="$HOME/.cloudflared/${TUNNEL_ID}.json"

# Create config
cat > "$HOME/.cloudflared/config.yml" << EOF
tunnel: ${TUNNEL_ID}
credentials-file: ${CREDENTIALS_FILE}

ingress:
  - hostname: ${TUNNEL_NAME}.yourdomain.com
    service: http://localhost:8000
  - service: http_status:404
EOF

# Extract token for Docker
echo ""
echo "🔑 Your tunnel credentials file: $CREDENTIALS_FILE"
echo ""
echo "For Docker deployment, extract the token:"
echo "  cat $CREDENTIALS_FILE | jq -r '.t'"
echo ""
echo "Then set it as CF_TUNNEL_TOKEN in your .env"
