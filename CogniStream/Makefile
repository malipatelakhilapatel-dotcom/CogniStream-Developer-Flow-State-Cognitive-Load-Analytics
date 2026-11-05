.PHONY: help install pipeline test backend frontend up down clean verify

help:
	@echo "CogniStream Management Commands:"
	@echo "  make install    - Install Python and Node.js dependencies"
	@echo "  make pipeline   - Run ingestion and flow analytics pipelines"
	@echo "  make test       - Run backend and engine automated test suites"
	@echo "  make backend    - Start local FastAPI development server"
	@echo "  make frontend   - Start local Vite React dashboard"
	@echo "  make up         - Start full stack using Docker Compose"
	@echo "  make down       - Stop all Docker Compose containers"
	@echo "  make verify     - Audit end-to-end data pipeline and API health"

install:
	pip install -r backend/requirements.txt
	cd frontend && npm install

pipeline:
	python scripts/run_pipeline.py

test:
	python -m pytest backend/tests/ ingestion/tests/ -v

backend:
	python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

frontend:
	cd frontend && npm run dev

up:
	docker-compose up --build

down:
	docker-compose down

verify:
	python scripts/verify_setup.py