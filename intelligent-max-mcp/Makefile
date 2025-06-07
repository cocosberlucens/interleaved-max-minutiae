.PHONY: help install install-dev test test-cov lint format type-check clean run debug docs pre-commit

# Default target
help:
	@echo "Available targets:"
	@echo "  install      - Install package in development mode"
	@echo "  install-dev  - Install package with development dependencies"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage report"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black and isort"
	@echo "  type-check   - Run mypy type checking"
	@echo "  clean        - Clean up generated files"
	@echo "  run          - Run the MCP server"
	@echo "  debug        - Run the MCP server with debugging"
	@echo "  docs         - Generate documentation"
	@echo "  pre-commit   - Set up pre-commit hooks"

install:
	pip install -e .

install-dev:
	pip install -e .[dev]
	pre-commit install

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src/ tests/
	pylint src/

format:
	black src/ tests/
	isort src/ tests/

type-check:
	mypy src/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/

run:
	python src/main.py --config config/config.development.yaml

debug:
	python -m pdb src/main.py --config config/config.development.yaml

docs:
	cd docs && make html

pre-commit:
	pre-commit install
	pre-commit run --all-files

# Environment management
env-create:
	conda create -n intelligent-max-mcp python=3.11 -y

env-update:
	conda env update -f environment.yml

env-export:
	conda env export > environment.yml

# Quick development workflow
dev-setup: env-create install-dev pre-commit
	@echo "Development environment setup complete!"

# Production build
build:
	python setup.py sdist bdist_wheel

# Check everything before commit
check-all: format lint type-check test
	@echo "All checks passed!"