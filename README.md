# BMDR Setup

A general-purpose project boilerplate for modern web applications with autonomous deployment capabilities.

## 🎯 What This Provides

- **FastAPI** backend with auto-generated OpenAPI docs
- **Docker** containerization with multi-stage builds
- **Docker Compose** for local development and production
- **GitHub Actions** CI/CD pipeline
- **Cloudflare Tunnel** integration for instant public URLs
- **Health checks** and monitoring endpoints
- **Environment-based configuration**
- **Autonomous deployment** ready — designed for AI agent pipelines

## 🚀 Quick Start

### Prerequisites
- Docker + Docker Compose
- GitHub account
- Cloudflare account (for tunnel)

### Local Development
```bash
git clone https://github.com/YOUR_ORG/bmdr-setup.git my-project
cd my-project
cp .env.example .env
# Edit .env with your values
docker-compose up --build
```

App will be available at: http://localhost:8000

### Deploy to Production
```bash
# Set your Cloudflare tunnel token
export CF_TUNNEL_TOKEN="your-token-here"

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

## 📁 Project Structure

```
.
├── app/                    # Application code
│   ├── __init__.py
│   ├── main.py            # FastAPI entry point
│   ├── config.py          # Configuration management
│   ├── routers/           # API route modules
│   ├── models/            # Data models
│   └── services/          # Business logic
├── tests/                 # Test suite
├── scripts/               # Deployment scripts
│   ├── deploy.sh
│   └── setup-tunnel.sh
├── .github/               # GitHub Actions workflows
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── docker/                # Docker configurations
│   ├── Dockerfile
│   └── Dockerfile.prod
├── docker-compose.yml     # Local development
├── docker-compose.prod.yml # Production deployment
├── .env.example           # Environment template
├── .dockerignore
├── .gitignore
└── README.md
```

## 🔧 Configuration

All configuration is environment-based. Copy `.env.example` to `.env` and customize:

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | `bmdr-app` |
| `APP_ENV` | Environment (dev/staging/prod) | `dev` |
| `APP_PORT` | HTTP port | `8000` |
| `LOG_LEVEL` | Logging level | `info` |
| `CF_TUNNEL_TOKEN` | Cloudflare tunnel token | (required for prod) |

## 🌐 Cloudflare Tunnel

This setup uses Cloudflare Tunnel to expose your app securely without opening firewall ports.

### Setup
1. Install `cloudflared`: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/
2. Create a tunnel: `cloudflared tunnel create bmdr-app`
3. Get your token from `~/.cloudflared/*.json`
4. Set `CF_TUNNEL_TOKEN` in your environment

### URLs
- Local: http://localhost:8000
- Public (via tunnel): https://your-domain.com

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

1. **CI** (`ci.yml`)
   - Runs on every PR
   - Lint, test, build Docker image
   - Security scan

2. **Deploy** (`deploy.yml`)
   - Runs on push to `main`
   - Builds and pushes Docker image
   - Deploys to target environment
   - Verifies health check

## 🏥 Health Checks

Built-in endpoints:
- `GET /health` — Basic health check
- `GET /ready` — Readiness probe (checks dependencies)
- `GET /metrics` — Prometheus-compatible metrics

## 🛠️ Customization

### Adding a New Route
```python
# app/routers/items.py
from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
async def list_items():
    return {"items": []}
```

Register in `app/main.py`:
```python
from app.routers import items
app.include_router(items.router)
```

### Changing the Tech Stack
This boilerplate uses FastAPI + Python, but the structure works for:
- Node.js + Express/Fastify
- Go + Gin/Fiber
- Ruby on Rails
- Any containerized app

Replace `app/` and `Dockerfile` with your stack.

## 📜 License

MIT — use freely for your projects.

---

Built for autonomous deployment pipelines. 🤖
