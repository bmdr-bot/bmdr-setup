# BMDR Setup - Deployment Guide

## 🚀 Quick Deploy on Your VPS

### 1. Clone the Repo

```bash
git clone https://github.com/bmdr-bot/bmdr-setup.git
cd bmdr-setup
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your values
nano .env
```

Required for production:
- `CF_TUNNEL_TOKEN` — Cloudflare tunnel token

### 3. Build and Run Locally

```bash
chmod +x scripts/*.sh
./scripts/run-local.sh
```

### 4. Deploy to Production

```bash
# Option A: Using deploy script
./scripts/deploy.sh production

# Option B: Using Docker Compose directly
docker-compose -f docker-compose.prod.yml up -d
```

## 🌐 Cloudflare Tunnel Setup

### Install cloudflared

```bash
# Download
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Or use the setup script
./scripts/setup-tunnel.sh bmdr-app
```

### Create Tunnel

```bash
cloudflared tunnel login
cloudflared tunnel create bmdr-app
cloudflared tunnel route dns bmdr-app app.yourdomain.com
```

### Get Token for Docker

```bash
cat ~/.cloudflared/*.json | jq -r '.t'
# Set this as CF_TUNNEL_TOKEN in .env
```

## 🔧 Docker Permission Fix (If Needed)

If you get permission denied on Docker socket:

```bash
# Add your user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Or run with sudo
sudo docker-compose up -d
```

## 📊 Monitoring

Check app status:
```bash
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f app
```

Health endpoints:
- http://localhost:8000/health/
- http://localhost:8000/health/ready
- http://localhost:8000/health/metrics

## 🔄 CI/CD

GitHub Actions workflows:
- **CI**: Runs on PR — lint, test, build
- **Deploy**: Runs on push to main — build, push, deploy

Required secrets for deploy:
- `DEPLOY_HOST` — your VPS IP
- `DEPLOY_USER` — SSH username
- `DEPLOY_KEY` — SSH private key
- `HEALTH_URL` — health check URL after deploy

## 🏗️ Creating a New Project from This Template

```bash
# Clone
git clone https://github.com/bmdr-bot/bmdr-setup.git my-new-project
cd my-new-project

# Remove git history
rm -rf .git
git init
git add .
git commit -m "Initial commit"

# Update names
find . -type f -exec sed -i 's/bmdr-setup/my-new-project/g' {} +

# Push to your repo
git remote add origin https://github.com/YOUR_ORG/my-new-project.git
git push -u origin main
```

---

Built for autonomous deployment. 🤖
