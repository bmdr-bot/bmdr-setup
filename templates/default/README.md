# $project_name

$description

## 🚀 Quick Start

```bash
# Local development
cp .env.example .env
docker-compose up --build

# Access app
open http://localhost:8000
```

## 📁 Project Structure

```
.
├── app/              # Application code
├── tests/            # Test suite
├── scripts/          # Deployment scripts
├── k8s/              # Kubernetes manifests
└── docker-compose.yml
```

## 🛠️ Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run locally
uvicorn app.main:app --reload
```

## 🌐 Deployment

### Docker Compose
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes
```bash
kubectl apply -k k8s/
```

## 📄 License

$license
