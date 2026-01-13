# FastAPI DevSecOps Demo

[![CI/CD Pipeline](https://github.com/CharithKapuluru/fastapi-devsecops-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/CharithKapuluru/fastapi-devsecops-demo/actions/workflows/ci.yml)
[![Semgrep Security](https://github.com/CharithKapuluru/fastapi-devsecops-demo/actions/workflows/semgrep.yml/badge.svg)](https://github.com/CharithKapuluru/fastapi-devsecops-demo/actions/workflows/semgrep.yml)
[![Trivy Security](https://github.com/CharithKapuluru/fastapi-devsecops-demo/actions/workflows/trivy.yml/badge.svg)](https://github.com/CharithKapuluru/fastapi-devsecops-demo/actions/workflows/trivy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready FastAPI microservice demonstrating **DevSecOps best practices** with automated security scanning, CI/CD, and containerization. Built to showcase cloud-native development skills for **Cloud Engineer**, **DevOps Engineer**, and **DevSecOps Engineer** roles.

---

## 🎯 Project Highlights

- ✅ **RESTful API** with FastAPI (OpenAPI/Swagger docs auto-generated)
- ✅ **Comprehensive Testing** with pytest (18 tests, 100% pass rate)
- ✅ **Code Quality** with Ruff linting and formatting
- ✅ **Containerization** with Docker (optimized multi-stage builds)
- ✅ **CI/CD Pipeline** with GitHub Actions (automated testing and deployment)
- ✅ **Security Scanning** with Semgrep (SAST for code vulnerabilities)
- ✅ **Container Security** with Trivy (vulnerability and misconfiguration detection)
- ✅ **Production Logging** with structured JSON logs
- ✅ **Health Checks** built-in for orchestration platforms

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         GitHub                              │
│  ┌───────────┐  ┌──────────┐  ┌────────────────────────┐  │
│  │  Push     │→ │ Actions  │→ │ Workflows              │  │
│  │  Code     │  │ Trigger  │  │ ├─ Lint & Test         │  │
│  └───────────┘  └──────────┘  │ ├─ Build & Push Docker │  │
│                                │ ├─ Semgrep SAST        │  │
│                                │ └─ Trivy Container Scan│  │
│                                └────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│             GitHub Container Registry (ghcr.io)             │
│  🐳 fastapi-devsecops-demo:latest                          │
│     - Python 3.12 runtime                                   │
│     - FastAPI application                                   │
│     - Production dependencies                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   Deployment Target                         │
│  AWS ECS | Google Cloud Run | Azure Container Instances    │
│  Kubernetes | Docker Swarm | Any container platform        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Docker (optional, for containerized deployment)
- Git

### Local Development

```bash
# Clone the repository
git clone https://github.com/CharithKapuluru/fastapi-devsecops-demo.git
cd fastapi-devsecops-demo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access the API
# - API: http://localhost:8000
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

### Docker Deployment

```bash
# Build the Docker image
docker build -t fastapi-devsecops-demo:latest .

# Run the container
docker run -d -p 8000:8000 --name fastapi-app fastapi-devsecops-demo:latest

# Or use the published image
docker pull ghcr.io/charithkapuluru/fastapi-devsecops-demo:latest
docker run -d -p 8000:8000 ghcr.io/charithkapuluru/fastapi-devsecops-demo:latest
```

### Using Makefile

```bash
make help          # Show all available commands
make run           # Run locally
make test          # Run tests
make lint          # Run linting
make format        # Format code
make docker-build  # Build Docker image
make docker-run    # Run Docker container
make docker-stop   # Stop and remove container
```

---

## 📡 API Endpoints

### Health Check
```bash
GET /health
```
Returns service health status. Used by load balancers and orchestration platforms.

**Response:**
```json
{
  "status": "ok"
}
```

### Get All Items
```bash
GET /items
```
Retrieves all items from the in-memory database.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "MacBook Pro 16-inch"
  }
]
```

### Create Item
```bash
POST /items
Content-Type: application/json

{
  "name": "Laptop",
  "description": "MacBook Pro 16-inch"
}
```

Creates a new item with auto-incrementing ID.

**Validation:**
- `name`: Required, 1-100 characters
- `description`: Optional, max 500 characters

**Response:**
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "MacBook Pro 16-inch"
}
```

---

## 🔧 Tech Stack

### Core Technologies
- **Python 3.12** - Modern Python with type hints
- **FastAPI 0.115+** - High-performance async web framework
- **Pydantic 2.10+** - Data validation using Python type annotations
- **Uvicorn 0.34+** - Lightning-fast ASGI server

### Development Tools
- **Pytest 8.3+** - Comprehensive testing framework
- **Ruff 0.9+** - Ultra-fast Python linter and formatter
- **Docker** - Containerization platform
- **Make** - Build automation

### CI/CD & Security
- **GitHub Actions** - CI/CD automation
- **Semgrep** - Static application security testing (SAST)
- **Trivy** - Container vulnerability scanning
- **GitHub Container Registry** - Docker image hosting

---

## 🧪 Testing

The project includes 18 comprehensive tests covering:
- Health endpoint functionality
- Item creation and retrieval
- Input validation (positive and negative cases)
- Edge cases (empty lists, max length, invalid types)
- API response formats

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=html

# Run specific test class
pytest tests/test_api.py::TestHealthEndpoint -v
```

**Test Results:**
```
18 passed in 0.33s
```

---

## 🔐 Security Features

### 1. Semgrep SAST Scanning
Automated static analysis for security vulnerabilities:
- SQL injection patterns
- Cross-Site Scripting (XSS)
- Hardcoded secrets
- Insecure cryptography
- Command injection
- OWASP Top 10 coverage

**Configuration:** `.github/workflows/semgrep.yml`

### 2. Trivy Container Scanning
Comprehensive container security:
- OS package vulnerabilities (Debian)
- Python dependency vulnerabilities
- Dockerfile misconfiguration detection
- Hardcoded secrets in image layers

**Configuration:** `.github/workflows/trivy.yml`

### 3. Code Quality Enforcement
- Ruff linting (700+ rule checks)
- Automated formatting validation
- Type checking with Pydantic
- Input validation on all endpoints

**View Security Results:** Check the **Security** tab on GitHub for detailed findings.

---

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for automated CI/CD:

### CI/CD Workflow (`ci.yml`)
**Triggers:** Push to main, Pull Requests

**Jobs:**
1. **Lint and Test**
   - Ruff linting checks
   - Ruff formatting validation
   - Pytest test suite (18 tests)

2. **Build and Push Docker** (main branch only)
   - Build Docker image with BuildKit
   - Push to GitHub Container Registry
   - Tag with: `latest`, `main`, `main-<sha>`

### Security Workflows

**Semgrep Scan** (`semgrep.yml`)
- Runs on: Push, PR, Daily (6 AM UTC)
- Scans: Python code for security vulnerabilities
- Output: GitHub Security tab (SARIF format)

**Trivy Scan** (`trivy.yml`)
- Runs on: Push, PR, Weekly (Sundays)
- Scans: Docker image and Dockerfile
- Output: GitHub Security tab (SARIF format)

---

## 📁 Project Structure

```
fastapi-devsecops-demo/
├── app/                      # Application source code
│   ├── __init__.py          # Package marker
│   ├── config.py            # Configuration and logging
│   ├── main.py              # FastAPI application and endpoints
│   └── models.py            # Pydantic models
├── tests/                    # Test suite
│   ├── __init__.py
│   └── test_api.py          # API endpoint tests (18 tests)
├── .github/
│   └── workflows/           # CI/CD workflows
│       ├── ci.yml           # Main CI/CD pipeline
│       ├── semgrep.yml      # Security scanning (SAST)
│       └── trivy.yml        # Container security scanning
├── Dockerfile               # Multi-stage Docker build
├── .dockerignore            # Docker build exclusions
├── .gitignore               # Git exclusions
├── .semgrepignore           # Semgrep exclusions
├── .trivyignore             # Trivy exclusions
├── Makefile                 # Build automation commands
├── pyproject.toml           # Ruff configuration
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## 🐳 Docker Details

### Image Specifications
- **Base Image:** `python:3.12-slim` (Debian-based, minimal)
- **Final Size:** ~190MB (optimized)
- **Exposed Port:** 8000
- **Health Check:** Automatic (30s interval)
- **User:** Root (can be changed for enhanced security)

### Dockerfile Highlights
- Layer caching optimization for fast rebuilds
- Non-buffered Python output for real-time logs
- No `.pyc` files for reduced image size
- Automated health checks via `/health` endpoint

### Environment Variables
- `PYTHONDONTWRITEBYTECODE=1` - Disable bytecode generation
- `PYTHONUNBUFFERED=1` - Enable real-time log output

---

## 📊 Logging

The application uses structured JSON logging for production observability:

```json
{
  "timestamp": "2026-01-12 19:10:34,300",
  "level": "INFO",
  "message": "Created item with ID 1: Test Item",
  "module": "app.config"
}
```

**Benefits:**
- Machine-parseable format
- Easy integration with log aggregators (CloudWatch, Datadog, Splunk)
- Searchable and filterable
- Production-ready

---

## 🚧 Future Enhancements

- [ ] Add PostgreSQL database integration
- [ ] Implement authentication (JWT tokens)
- [ ] Add rate limiting middleware
- [ ] Expand test coverage to 100%
- [ ] Add integration tests
- [ ] Deploy to AWS/GCP/Azure
- [ ] Add Prometheus metrics endpoint
- [ ] Implement caching with Redis
- [ ] Add OpenTelemetry tracing
- [ ] Create Kubernetes manifests

---

## 📝 Development Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Make changes and test locally**
   ```bash
   make lint    # Check code quality
   make test    # Run tests
   make format  # Auto-format code
   ```

3. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin feature/new-feature
   ```

4. **Create Pull Request**
   - Automated checks will run (lint, test, security scans)
   - Review results in GitHub Actions
   - Merge when all checks pass

5. **Automatic Deployment**
   - On merge to main, Docker image is built and pushed
   - Available at `ghcr.io/charithkapuluru/fastapi-devsecops-demo:latest`

---

## 🤝 Contributing

This is a portfolio demonstration project. For suggestions or improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Charith Kapuluru**
- GitHub: [@CharithKapuluru](https://github.com/CharithKapuluru)
- LinkedIn: [Connect with me](https://linkedin.com/in/charithkapuluru)

---

## 🙏 Acknowledgments

- FastAPI documentation and community
- GitHub Actions for CI/CD automation
- Semgrep and Trivy for security tooling
- Open-source community for excellent tools and libraries

---

**Built with Python 🐍 | Secured with DevSecOps 🔐 | Deployed with Docker 🐳**
