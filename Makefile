.PHONY: help run test lint format docker-build docker-run docker-stop clean

help:
	@echo "FastAPI DevSecOps Demo - Available Commands"
	@echo "==========================================="
	@echo "make run          - Run the FastAPI application locally"
	@echo "make test         - Run pytest tests"
	@echo "make lint         - Run ruff linting checks"
	@echo "make format       - Auto-format code with ruff"
	@echo "make docker-build - Build Docker image"
	@echo "make docker-run   - Run Docker container"
	@echo "make docker-stop  - Stop and remove Docker container"
	@echo "make clean        - Remove Python artifacts and caches"

run:
	@echo "Starting FastAPI application..."
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	@echo "Running tests..."
	. venv/bin/activate && pytest tests/ -v

lint:
	@echo "Running linting checks..."
	ruff check app/ tests/

format:
	@echo "Formatting code..."
	ruff format app/ tests/

docker-build:
	@echo "Building Docker image..."
	docker build -t fastapi-devsecops-demo:latest .

docker-run:
	@echo "Running Docker container..."
	docker run -d -p 8000:8000 --name fastapi-devsecops-demo fastapi-devsecops-demo:latest

docker-stop:
	@echo "Stopping Docker container..."
	docker stop fastapi-devsecops-demo || true
	docker rm fastapi-devsecops-demo || true

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleanup complete!"
