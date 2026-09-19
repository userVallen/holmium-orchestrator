.PHONY: install run dev test vet lint clean

TIMESTAMP = $(shell date "+%H:%M:%S") 

# Installation
install:
	@echo "[ $(TIMESTAMP)] Installing frontend dependencies..."
	@cd frontend && pnpm install --silent
	@echo "[ $(TIMESTAMP)] Frontend dependencies installed. ✅"

	@echo "[ $(TIMESTAMP)] Checking backend virtual environment..."
	@cd backend && \
	if [ ! -d "venv" ]; then \
		python3 -m venv venv; \
		echo "[ $(TIMESTAMP)] Virtual environment created. ✅"; \
	else \
		echo "[ $(TIMESTAMP)] Virtual environment already exists, skipping creation. ⏩"; \
	fi && \
	echo "[ $(TIMESTAMP)] Installing backend dependencies..." && \
	./venv/bin/pip install -q -r requirements.txt
	@echo "[ $(TIMESTAMP)] Backend dependencies installed. ✅"

# Running
run-backend:
	@echo "[ $(TIMESTAMP)] Starting backend server..."
	@PYTHONPATH=backend ./backend/venv/bin/uvicorn app.main:app
	@echo "[ $(TIMESTAMP)] Backend server is live. ✅"

run-frontend:
	@echo "[ $(TIMESTAMP)] Starting frontend server..."
	@cd frontend && pnpm build && pnpm start
	@echo "[ $(TIMESTAMP)] Frontend server is live. ✅"

# Development
dev-backend: 
	@echo "[ $(TIMESTAMP)] Starting backend development server..."
	@PYTHONPATH=backend ./backend/venv/bin/uvicorn app.main:app --reload
	@echo "[ $(TIMESTAMP)] Backend development server is live. ✅"

dev-frontend:
	@echo "[ $(TIMESTAMP)] Starting frontend development server..."
	@cd frontend && pnpm dev
	@echo "[ $(TIMESTAMP)] Frontend development server is live. ✅"

# Testing
test: test-backend test-frontend

test-backend:
	@echo "[ $(TIMESTAMP)] Running backend tests..." 
	@cd backend && ./venv/bin/pytest
	@echo "[ $(TIMESTAMP)] Backend tests complete. ✅"

test-frontend:
	@echo "[ $(TIMESTAMP)] Running frontend tests..."
	@cd frontend && pnpm test --watchAll=false
	@echo "[ $(TIMESTAMP)] Frontend tests complete. ✅"

# Vetting
vet: vet-backend vet-frontend

vet-backend:
	@echo "[ $(TIMESTAMP)] Vetting backend code (Ruff / Type checking)..."
	@cd backend && ./venv/bin/ruff check .
	@cd backend && ./venv/bin/mypy . --ignore-missing-imports
	@echo "[ $(TIMESTAMP)] Backend vetting complete. ✅"

vet-frontend:
	@echo "[ $(TIMESTAMP)] Vetting frontend code (Type check & Lint)..."
	@cd frontend && pnpm tsc --noEmit
	@cd frontend && pnpm lint
	@echo "[ $(TIMESTAMP)] Frontend vetting complete. ✅"

# Linting
lint: lint-backend lint-frontend
	@echo "[ $(TIMESTAMP)] Linting complete. ✏️"

lint-backend:
	@echo "[ $(TIMESTAMP)] Linting backend code..."
	@cd backend && ./venv/bin/ruff check
	@echo "[ $(TIMESTAMP)] Backend linting complete. ✏️"

lint-backend-fix:
	@echo "[ $(TIMESTAMP)] Auto-fixing backend code..."
	@cd backend && ./venv/bin/ruff check --fix
	@echo "[ $(TIMESTAMP)] Backend linting complete. ✏️"

lint-frontend:
	@echo "[ $(TIMESTAMP)] Linting frontend code..."
	@cd frontend && pnpm lint
	@echo "[ $(TIMESTAMP)] Frontend linting complete. ✏️"

# Cleaning
clean:
	@echo "[ $(TIMESTAMP)] Cleaning backend cache files..."
	@find backend -type d \( -name "__pycache__" -o -name ".pytest_cache" -o -name ".mypy_cache" -o name ".ruff_cache" -o -name "venv" \) -exec rm -rf {} +
	@echo "[ $(TIMESTAMP)] Cleaning frontend build artifacts..."
	@rm -rf frontend/.next frontend/dist frontend/node_modules
	@echo "[ $(TIMESTAMP)] Cleanup complete. 🧹"