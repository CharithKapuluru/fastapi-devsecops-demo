# Phase 4: Docker Containerization

## What is Phase 4 About?

Phase 4 packages your application into a **Docker container** - a portable box that includes your app and everything it needs to run.

**The goal:** Your app runs exactly the same way on any computer, any server, anywhere in the world.

---

## The Problem Docker Solves

### The "Works on My Machine" Problem

Classic developer nightmare:

```
Developer: "The app works perfectly on my laptop!"
Server: "App crashed. Missing dependency."
Developer: "But it works on my machine..."
```

**Why does this happen?**

Your laptop has:
- Python 3.12
- Specific libraries installed
- Certain environment variables
- macOS operating system

The server has:
- Python 3.9 (different version!)
- Missing some libraries
- Different environment
- Linux operating system

**Same code, different environments = different results.**

---

## What is Docker?

Docker is a tool that packages your app + its environment into a **container**.

### Simple Analogy: Shipping Containers

Before shipping containers existed:
- Loading a ship took weeks
- Items got damaged, lost, stolen
- Different ports needed different equipment

After shipping containers:
- Standard box fits any ship, truck, or train
- Contents protected
- Load/unload anywhere the same way

**Docker does the same for software:**

| Shipping | Docker |
|----------|--------|
| Physical goods | Your application |
| Shipping container | Docker container |
| Ship, truck, train | Any server, cloud, laptop |
| Same box works everywhere | Same container runs everywhere |

---

## Key Docker Concepts

### Image vs Container

**Image** = A recipe/blueprint (like a cake recipe)
**Container** = A running instance (like an actual cake)

```
Dockerfile → builds → Image → runs → Container

(Recipe)              (Blueprint)     (Running App)
```

You build an image once. You can run many containers from it.

---

### What's Inside a Container?

```
┌─────────────────────────────────────┐
│         Docker Container            │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ Your App (app/main.py)      │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │ Python 3.12                 │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │ FastAPI, Uvicorn, etc.      │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │ Minimal Linux OS            │   │
│  └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

Everything needed to run your app is inside the container.

---

## What We Built

### File 1: Dockerfile

The Dockerfile is a **recipe** that tells Docker how to build your image.

```dockerfile
# Start with Python 3.12 (slim = smaller size)
FROM python:3.12-slim

# Create /app folder inside container
WORKDIR /app

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Show print statements immediately (important for logs)
ENV PYTHONUNBUFFERED=1

# Copy requirements.txt first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY app/ ./app/

# Tell Docker this app uses port 8000
EXPOSE 8000

# Health check - Docker will verify app is healthy
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Command to run when container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### Breaking Down Each Line

**`FROM python:3.12-slim`**
- Start with an official Python image
- `slim` version is smaller (fewer unnecessary tools)
- This gives us Python pre-installed

**`WORKDIR /app`**
- Create and enter `/app` directory
- All following commands run from here

**`ENV PYTHONDONTWRITEBYTECODE=1`**
- Don't create `.pyc` files (compiled Python)
- Keeps container cleaner

**`ENV PYTHONUNBUFFERED=1`**
- Print output immediately, don't buffer
- Critical for seeing logs in real-time

**`COPY requirements.txt .`**
- Copy requirements file into container
- Done separately for **layer caching** (explained below)

**`RUN pip install ...`**
- Install Python dependencies
- `--no-cache-dir` saves space

**`COPY app/ ./app/`**
- Copy your application code into container

**`EXPOSE 8000`**
- Document that this app uses port 8000
- Doesn't actually open the port (just documentation)

**`HEALTHCHECK`**
- Docker periodically checks if app is healthy
- Calls `/health` endpoint every 30 seconds
- If it fails 3 times, container marked unhealthy

**`CMD ["uvicorn", ...]`**
- Command to run when container starts
- Starts your FastAPI app

---

### File 2: .dockerignore

Like `.gitignore` but for Docker. Tells Docker what NOT to copy into the image.

```
.git
__pycache__/
venv/
tests/
*.md
.github/
```

**Why exclude these?**
- `.git` - Not needed to run app, wastes space
- `venv/` - We install fresh in container
- `tests/` - Not needed in production
- `*.md` - Documentation not needed to run

**Smaller image = faster deployments.**

---

## Layer Caching (Important Optimization)

Docker builds images in **layers**. Each instruction creates a layer.

**Why we copy requirements.txt first:**

```dockerfile
COPY requirements.txt .          # Layer 1
RUN pip install -r requirements.txt  # Layer 2
COPY app/ ./app/                 # Layer 3
```

**Scenario: You change code in app/main.py**

- Layer 1: requirements.txt unchanged → **Use cached layer**
- Layer 2: Dependencies unchanged → **Use cached layer**
- Layer 3: app/ changed → Rebuild this layer only

**Result:** Rebuild takes seconds, not minutes!

**If we did it wrong:**

```dockerfile
COPY . .                         # Copy everything
RUN pip install -r requirements.txt
```

Now ANY change invalidates the cache. Every build reinstalls all dependencies.

---

## Docker Commands

### Build the Image
```bash
docker build -t fastapi-devsecops .
```
- `-t fastapi-devsecops` = Name (tag) the image
- `.` = Use current directory's Dockerfile

### Run a Container
```bash
docker run -d -p 8000:8000 --name myapp fastapi-devsecops
```
- `-d` = Run in background (detached)
- `-p 8000:8000` = Map port 8000 on your machine to port 8000 in container
- `--name myapp` = Name the container

### See Running Containers
```bash
docker ps
```

### Stop the Container
```bash
docker stop myapp
```

### View Logs
```bash
docker logs myapp
```

---

## Makefile Commands We Added

```makefile
docker-build:
    docker build -t fastapi-devsecops-demo .

docker-run:
    docker run -d -p 8000:8000 --name fastapi-app fastapi-devsecops-demo

docker-stop:
    docker stop fastapi-app && docker rm fastapi-app
```

Now just run:
```bash
make docker-build   # Build the image
make docker-run     # Start the container
make docker-stop    # Stop and remove container
```

---

## Visual Flow

```
┌─────────────────┐     docker build     ┌─────────────────┐
│                 │ ──────────────────►  │                 │
│   Dockerfile    │                      │   Docker Image  │
│                 │                      │                 │
└─────────────────┘                      └────────┬────────┘
                                                  │
                                           docker run
                                                  │
                                                  ▼
                                         ┌─────────────────┐
                                         │                 │
                                         │   Container     │
                                         │   (Running!)    │
                                         │                 │
                                         └─────────────────┘
```

---

## Real-World Usage

### Development
```bash
make docker-build
make docker-run
# Test at http://localhost:8000
make docker-stop
```

### Production (AWS, Google Cloud, etc.)
1. Build image
2. Push to container registry (like Docker Hub or AWS ECR)
3. Cloud service pulls image and runs it

**Same image runs in development AND production = no surprises!**

---

## Why HEALTHCHECK Matters

Without health check:
```
Container running → App crashed inside → Container still "running" → Users get errors
```

With health check:
```
Container running → App crashed → Health check fails → Docker knows → Can auto-restart
```

The health check calls your `/health` endpoint (from Phase 1). Now you see why we built it!

---

## Common Mistakes to Avoid

### Mistake 1: Using full Python image
```dockerfile
FROM python:3.12      # 1GB+ image size
FROM python:3.12-slim # ~150MB image size
```
Always use `slim` unless you need specific tools.

### Mistake 2: Not using .dockerignore
Copies unnecessary files → Larger image → Slower builds/deployments

### Mistake 3: Running as root
Production containers should use non-root user for security. (We simplified this for MVP.)

### Mistake 4: No layer caching
Copy requirements.txt separately to leverage caching.

### Mistake 5: Hardcoding configuration
Use environment variables for things that change between environments.

---

## Production-Ready Checklist (Phase 4)

✅ **Dockerfile created** - Complete build recipe
✅ **Slim base image** - python:3.12-slim for smaller size
✅ **Layer caching** - requirements.txt copied first
✅ **Environment variables** - PYTHONUNBUFFERED for proper logging
✅ **.dockerignore** - Excludes unnecessary files
✅ **HEALTHCHECK** - Docker monitors app health
✅ **EXPOSE** - Port documented
✅ **Makefile commands** - Easy build/run/stop

---

## Key Takeaway

**Docker ensures consistency.**

"Works on my machine" becomes "Works on EVERY machine" because the machine is inside the container.

Every professional deployment uses containers. Kubernetes, AWS ECS, Google Cloud Run - they all run Docker containers.

---

## Next Steps

Phase 5 adds **CI/CD with GitHub Actions** - automatically building, testing, and deploying your containerized app when you push code.
