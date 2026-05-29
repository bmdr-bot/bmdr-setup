# BMDR Setup

A general-purpose project boilerplate with CLI tooling for modern web applications and autonomous deployment pipelines.

## 🎯 What This Provides

- **FastAPI** backend with auto-generated OpenAPI docs
- **Docker** containerization with multi-stage builds
- **Docker Compose** for local development and production
- **GitHub Actions** CI/CD pipeline
- **Cloudflare Tunnel** integration for instant public URLs
- **Kubernetes** manifests with Kustomize
- **Health checks** and monitoring endpoints
- **Environment-based configuration**
- **BMDR CLI** for project scaffolding and management
- **PR/Issue templates** for consistent workflows
- **Hermes skill templates** for AI agent integration

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker + Docker Compose
- GitHub account
- Cloudflare account (for tunnel)

### Install BMDR CLI

```bash
git clone https://github.com/bmdr-bot/bmdr-setup.git
cd bmdr-setup
pip install -e .
```

### Initialize Configuration

```bash
bmdr init
```

### Create a New Project

```bash
# Create from default template
bmdr create my-awesome-app --github

# Create with specific template
bmdr create my-api --template api --github --protect

# Create private repo
bmdr create my-secret-project --private --github
```

## 📋 BMDR CLI Commands

### `bmdr init`
Initialize BMDR CLI configuration (GitHub org, projects directory, defaults).

### `bmdr create <name>`
Create a new project from template.

**Options:**
- `--template, -t` — Template to use (default, api, microservice)
- `--dir, -d` — Target directory
- `--author, -a` — Project author
- `--description` — Project description
- `--github, -g` — Create GitHub repository
- `--private` — Private repository
- `--org` — Use organization account
- `--protect` — Enable branch protection

### `bmdr template list`
List available project templates.

### `bmdr deploy --target <target>`
Deploy project to target environment.

**Targets:**
- `docker` — Docker Compose deployment
- `kubernetes` — Kubernetes deployment
- `cloudflare` — Start Cloudflare tunnel

### `bmdr skill list`
List installed Hermes skills.

### `bmdr pr <title>`
Create a pull request from template.

**Options:**
- `--head` — Head branch (required)
- `--base` — Base branch (default: main)
- `--template, -t` — PR template (default, feature, bugfix, hotfix, release)
- `--description, -d` — PR description
- `--create, -c` — Create on GitHub
- `--repo, -r` — Repository name

## 📁 Project Structure

```
.
├── bmdr_cli/              # CLI source code
│   ├── __init__.py
│   ├── commands.py        # CLI commands
│   ├── config.py          # Configuration management
│   ├── github_ops.py      # GitHub API operations
│   └── templates.py       # Template rendering engine
├── templates/             # Project templates
│   ├── default/           # Default FastAPI project
│   ├── pr/                # PR templates
│   ├── issue/             # Issue templates
│   └── skill/             # Hermes skill templates
├── app/                   # Example application
├── tests/                 # Test suite
├── scripts/               # Deployment scripts
├── k8s/                   # Kubernetes manifests
├── .github/workflows/     # GitHub Actions
├── docker-compose.yml     # Local development
├── docker-compose.prod.yml # Production
├── Dockerfile             # Multi-stage build
├── requirements.txt
├── pyproject.toml
├── setup.py               # CLI package setup
└── README.md
```

## 🎨 Templates

### Project Templates
- **default** — Basic FastAPI app with health checks
- **api** — Full API with CRUD, auth, database
- **microservice** — Lightweight service template

### PR Templates
- **default** — Standard PR template
- **feature** — Feature PR with testing checklist
- **bugfix** — Bug fix PR with root cause analysis
- **hotfix** — Expedited hotfix template
- **release** — Release PR with deployment notes

### Issue Templates
- **bug** — Bug report with reproduction steps
- **feature** — Feature request with problem statement

### Skill Templates
- Hermes SKILL.md format
- Setup scripts
- Best practices built-in

## 🌐 Cloudflare Tunnel

This setup uses Cloudflare Tunnel to expose your app securely without opening firewall ports.

### Setup
```bash
bmdr deploy --target cloudflare
```

Or manually:
```bash
./scripts/setup-tunnel.sh my-app
```

## 🔧 Development

### Run Tests
```bash
pytest tests/ -v
```

### Lint
```bash
ruff check app/ bmdr_cli/
```

### Type Check
```bash
mypy app/ bmdr_cli/
```

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
- `GET /ready` — Readiness probe
- `GET /metrics` — Prometheus-compatible metrics

## 🛠️ Customization

### Adding a New Project Template

1. Create directory in `templates/<name>/`
2. Add template files with `$variable` placeholders
3. Use `bmdr create <name> --template <name>`

### Adding a New PR Template

1. Create file in `templates/pr/<name>.md`
2. Use `{{variable}}` for runtime substitution
3. Use `bmdr pr <title> --template <name>`

## 📜 License

MIT — use freely for your projects.

---

Built for autonomous deployment pipelines. 🤖
