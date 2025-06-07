# Development Environment Setup Guide

## Intelligent Max MCP Server Development Environment

**Complete setup guide for developing the Intelligent Max MCP Server on macOS**

*Tested on: MacBook Air (Intel i5, 8GB RAM) running macOS*

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Python Environment Setup](#python-environment-setup)
- [Project Structure Setup](#project-structure-setup)
- [VS Code Configuration](#vs-code-configuration)
- [Development Dependencies](#development-dependencies)
- [Initial Project Files](#initial-project-files)
- [Git Configuration](#git-configuration)
- [Development Workflow](#development-workflow)
- [Testing Setup](#testing-setup)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **macOS**: 10.15+ (Catalina or later)
- **Memory**: 8GB+ RAM (minimum for comfortable development)
- **Storage**: 2GB+ free space for development environment
- **Internet**: Stable connection for package downloads and documentation access

### Required Software

#### 1. Homebrew (if not installed)
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Verify installation
brew --version
```

#### 2. Git (usually pre-installed)
```bash
# Verify Git installation
git --version

# If not installed
brew install git
```

#### 3. Anaconda Python Distribution
```bash
# Download and install Anaconda from: https://www.anaconda.com/products/distribution
# Or install via Homebrew
brew install --cask anaconda

# Add conda to PATH (add to ~/.zshrc or ~/.bash_profile)
export PATH="/usr/local/anaconda3/bin:$PATH"

# Reload shell configuration
source ~/.zshrc  # or source ~/.bash_profile

# Verify installation
conda --version
python --version
```

#### 4. Node.js (for any future web interface needs)
```bash
# Install Node.js via Homebrew
brew install node

# Verify installation
node --version
npm --version
```

#### 5. VS Code
```bash
# Install via Homebrew
brew install --cask visual-studio-code

# Or download from: https://code.visualstudio.com/
```

---

## Python Environment Setup

### 1. Create Dedicated Conda Environment

```bash
# Create new environment with Python 3.11
conda create -n intelligent-max-mcp python=3.11 -y

# Activate environment
conda activate intelligent-max-mcp

# Verify Python version
python --version  # Should show Python 3.11.x

# Install conda-forge packages for better compatibility
conda config --add channels conda-forge
conda config --set channel_priority strict
```

### 2. Environment Management

```bash
# Save environment specification
conda env export > environment.yml

# Recreate environment from specification (useful for new machines)
conda env create -f environment.yml

# List all environments
conda env list

# Remove environment (if needed)
conda env remove -n intelligent-max-mcp
```

### 3. Shell Configuration

Add to your `~/.zshrc` or `~/.bash_profile`:

```bash
# Conda initialization
__conda_setup="$('/usr/local/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/usr/local/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/usr/local/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/usr/local/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup

# Auto-activate intelligent-max-mcp environment for this project
alias cdmcp="cd ~/path/to/interleaved-max-minutiae/intelligent-max-mcp && conda activate intelligent-max-mcp"
```

---

## Project Structure Setup

### 1. Clone Repository and Navigate

```bash
# Clone the repository (if not already done)
git clone https://github.com/cocosberlucens/interleaved-max-minutiae.git
cd interleaved-max-minutiae/intelligent-max-mcp

# Ensure we're in the correct environment
conda activate intelligent-max-mcp
```

### 2. Create Project Directory Structure

```bash
# Create comprehensive directory structure
mkdir -p {src/{core,knowledge,generation,api},tests/{unit,integration,fixtures},examples/{basic,advanced,temporal},docs/{api,guides,knowledge_sources},logs,cache,config}

# Create __init__.py files for Python packages
touch src/__init__.py
touch src/core/__init__.py
touch src/knowledge/__init__.py
touch src/generation/__init__.py
touch src/api/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py

# Create main source files
touch src/main.py
touch src/core/mcp_server.py
touch src/knowledge/engine.py
touch src/knowledge/cycling74_connector.py
touch src/knowledge/minutiae_connector.py
touch src/generation/patcher_generator.py
touch src/generation/temporal_scaffolding.py
touch src/api/functions.py

# Create configuration files
touch config/config.yaml
touch config/config.development.yaml
touch config/config.testing.yaml

# Create documentation files
touch docs/api/README.md
touch docs/guides/getting_started.md
touch docs/knowledge_sources/cycling74_integration.md

# Create example files
touch examples/basic/simple_patcher.py
touch examples/advanced/temporal_system.py
touch examples/temporal/function_generator.py
```

### 3. Verify Structure

```bash
# Display the created structure
tree . -I '__pycache__|*.pyc|.git'
```

Expected structure:
```
.
├── API_SPECIFICATION.md
├── README.md
├── ROADMAP.md
├── cache/
├── config/
│   ├── config.development.yaml
│   ├── config.testing.yaml
│   └── config.yaml
├── docs/
│   ├── api/
│   │   └── README.md
│   ├── guides/
│   │   └── getting_started.md
│   └── knowledge_sources/
│       └── cycling74_integration.md
├── examples/
│   ├── advanced/
│   │   └── temporal_system.py
│   ├── basic/
│   │   └── simple_patcher.py
│   └── temporal/
│       └── function_generator.py
├── logs/
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── functions.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── mcp_server.py
│   ├── generation/
│   │   ├── __init__.py
│   │   ├── patcher_generator.py
│   │   └── temporal_scaffolding.py
│   ├── knowledge/
│   │   ├── __init__.py
│   │   ├── cycling74_connector.py
│   │   ├── engine.py
│   │   └── minutiae_connector.py
│   └── main.py
└── tests/
    ├── __init__.py
    ├── fixtures/
    ├── integration/
    │   └── __init__.py
    └── unit/
        └── __init__.py
```

---

## Development Dependencies

### 1. Core MCP Dependencies

```bash
# Activate environment
conda activate intelligent-max-mcp

# Install MCP SDK and core dependencies
pip install anthropic-mcp-sdk
pip install mcp

# Verify MCP installation
python -c "import mcp; print('MCP installed successfully')"
```

### 2. Project-Specific Dependencies

```bash
# Web scraping and HTTP requests
pip install requests beautifulsoup4 lxml aiohttp

# Data processing and validation
pip install jsonschema pydantic numpy pandas

# File and repository management
pip install gitpython pathlib2 watchdog

# Configuration management
pip install pyyaml python-dotenv

# Async support
pip install asyncio aiofiles

# Documentation parsing
pip install markdown mistune

# Optional: Enhanced JSON handling
pip install orjson  # Faster JSON parsing
```

### 3. Development and Testing Dependencies

```bash
# Testing framework
pip install pytest pytest-asyncio pytest-cov pytest-mock

# Code quality
pip install black isort mypy flake8 pylint

# Pre-commit hooks
pip install pre-commit

# Documentation generation
pip install sphinx sphinx-rtd-theme

# Debugging and profiling
pip install ipdb pdb++ memory-profiler

# Jupyter notebook support (for experimentation)
pip install jupyter notebook ipykernel

# Add kernel to Jupyter
python -m ipykernel install --user --name intelligent-max-mcp --display-name "Intelligent Max MCP"
```

### 4. Create Requirements Files

```bash
# Generate current requirements
pip freeze > requirements.txt

# Create development requirements
cat > requirements-dev.txt << EOF
pytest>=7.0.0
pytest-asyncio>=0.20.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
black>=23.0.0
isort>=5.12.0
mypy>=1.0.0
flake8>=6.0.0
pylint>=2.16.0
pre-commit>=3.0.0
sphinx>=6.0.0
sphinx-rtd-theme>=1.2.0
ipdb>=0.13.0
memory-profiler>=0.60.0
jupyter>=1.0.0
notebook>=6.5.0
ipykernel>=6.20.0
EOF

# Install development dependencies
pip install -r requirements-dev.txt
```

---

## VS Code Configuration

### 1. Install Essential Extensions

```bash
# Python development
code --install-extension ms-python.python
code --install-extension ms-python.mypy-type-checker
code --install-extension ms-python.black-formatter
code --install-extension ms-python.isort
code --install-extension ms-python.pylint

# Jupyter support
code --install-extension ms-toolsai.jupyter

# Git and version control
code --install-extension eamodio.gitlens
code --install-extension mhutchie.git-graph

# YAML and JSON
code --install-extension redhat.vscode-yaml
code --install-extension vscode-icons-team.vscode-icons

# Documentation
code --install-extension davidanson.vscode-markdownlint
code --install-extension yzhang.markdown-all-in-one

# Additional utilities
code --install-extension ms-vscode.vscode-json
code --install-extension bradlc.vscode-tailwindcss  # For any future web UI
```

### 2. Create VS Code Settings

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "~/anaconda3/envs/intelligent-max-mcp/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.terminal.activateEnvInCurrentTerminal": true,
    
    // Linting and formatting
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.mypyEnabled": true,
    "python.linting.flake8Enabled": false,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    
    // Editor settings
    "editor.formatOnSave": true,
    "editor.formatOnPaste": true,
    "editor.rulers": [88],
    "editor.tabSize": 4,
    "editor.insertSpaces": true,
    
    // File associations and exclusions
    "files.associations": {
        "*.yaml": "yaml",
        "*.yml": "yaml"
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/.pytest_cache": true,
        "**/node_modules": true,
        "**/.git": false
    },
    
    // Search exclusions
    "search.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/logs": true,
        "**/cache": true
    },
    
    // Terminal settings
    "terminal.integrated.defaultProfile.osx": "zsh",
    "terminal.integrated.env.osx": {
        "PYTHONPATH": "${workspaceFolder}/src"
    },
    
    // Testing configuration
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "tests",
        "--verbose"
    ],
    "python.testing.unittestEnabled": false,
    
    // Documentation
    "markdown.preview.breaks": true,
    "markdown.preview.linkify": true,
    
    // Git settings
    "git.enableSmartCommit": true,
    "git.confirmSync": false,
    "gitlens.currentLine.enabled": false,
    
    // Workspace specific
    "workbench.colorTheme": "Default Dark+",
    "workbench.iconTheme": "vscode-icons",
    
    // IntelliSense and autocomplete
    "python.analysis.autoImportCompletions": true,
    "python.analysis.typeCheckingMode": "basic"
}
```

### 3. Create Debug Configuration

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run MCP Server",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/main.py",
            "args": ["--config", "config/config.development.yaml"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src",
                "ENVIRONMENT": "development"
            },
            "stopOnEntry": false,
            "justMyCode": false
        },
        {
            "name": "Debug Knowledge Engine",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/knowledge/engine.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src"
            }
        },
        {
            "name": "Test Knowledge Engine",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/tests/unit/test_knowledge_engine.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src"
            }
        },
        {
            "name": "Debug Patcher Generation",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/generation/patcher_generator.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src"
            }
        },
        {
            "name": "Run Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["tests/", "-v"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src"
            }
        }
    ]
}
```

### 4. Create Tasks Configuration

Create `.vscode/tasks.json`:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Install Dependencies",
            "type": "shell",
            "command": "pip",
            "args": ["install", "-r", "requirements.txt"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "Run Tests",
            "type": "shell",
            "command": "pytest",
            "args": ["tests/", "-v"],
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "Format Code",
            "type": "shell",
            "command": "black",
            "args": ["src/", "tests/"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "silent",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "Sort Imports",
            "type": "shell",
            "command": "isort",
            "args": ["src/", "tests/"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "silent",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "Type Check",
            "type": "shell",
            "command": "mypy",
            "args": ["src/"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "Lint Code",
            "type": "shell",
            "command": "pylint",
            "args": ["src/"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        }
    ]
}
```

---

## Initial Project Files

### 1. Setup.py

Create `setup.py`:

```python
"""
Setup configuration for Intelligent Max MCP Server
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="intelligent-max-mcp",
    version="0.1.0",
    description="Intelligent Max/MSP MCP Server with living knowledge base",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Corrado (Coco) & Claude",
    author_email="",
    url="https://github.com/cocosberlucens/interleaved-max-minutiae",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "anthropic-mcp-sdk>=0.1.0",
        "mcp>=0.1.0",
        "requests>=2.28.0",
        "jsonschema>=4.0.0",
        "pydantic>=2.0.0",
        "numpy>=1.21.0",
        "beautifulsoup4>=4.11.0",
        "lxml>=4.9.0",
        "gitpython>=3.1.0",
        "aiohttp>=3.8.0",
        "aiofiles>=22.0.0",
        "pyyaml>=6.0.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.20.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
            "pylint>=2.16.0",
            "pre-commit>=3.0.0",
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "jupyter>=1.0.0",
            "notebook>=6.5.0",
            "ipykernel>=6.20.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "notebook>=6.5.0",
            "ipykernel>=6.20.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "intelligent-max-mcp=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json", "*.md"],
    },
)
```

### 2. Configuration Files

Create `config/config.yaml`:

```yaml
# Intelligent Max MCP Server Configuration
server:
  name: "intelligent-max-mcp"
  version: "0.1.0"
  description: "Intelligent Max/MSP Documentation and Patcher Generation"
  host: "localhost"
  port: 8000
  debug: false

# Knowledge source configurations
knowledge_sources:
  cycling74_docs:
    base_url: "https://docs.cycling74.com"
    cache_duration: 3600  # 1 hour in seconds
    max_concurrent_requests: 5
    request_timeout: 30
    retry_attempts: 3
    retry_delay: 1.0
    
  minutiae_repo:
    local_path: "../"  # Relative to project root
    auto_update: true
    update_interval: 300  # 5 minutes in seconds
    watch_for_changes: true
    
  # Future: Additional knowledge sources
  max_forum:
    enabled: false
    base_url: "https://cycling74.com/forums"
    
  youtube_tutorials:
    enabled: false
    api_key: ""  # To be set in environment

# Patcher generation settings
patcher_generation:
  defaults:
    window_size: [800, 600]
    grid_size: 20
    object_spacing: 50
    font_size: 12
    
  templates:
    basic:
      window_size: [600, 400]
      include_dac: true
    
    temporal_scaffolding:
      window_size: [1200, 800]
      include_jsui: true
      include_transport: true
      
    sample_manipulation:
      window_size: [1000, 700]
      include_buffers: true
      include_waveform: true

# Pattern recognition and learning
pattern_recognition:
  confidence_threshold: 0.8
  learning_rate: 0.1
  max_patterns_cache: 1000
  pattern_expiry: 86400  # 24 hours
  auto_enhance_knowledge: true
  
# Caching configuration
cache:
  directory: "./cache"
  max_size_mb: 100
  cleanup_interval: 3600  # 1 hour
  
# Logging configuration
logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "./logs/intelligent-max.log"
  max_file_size_mb: 10
  backup_count: 5
  console_output: true
  
# Development settings
development:
  auto_reload: true
  profiling_enabled: false
  debug_knowledge_engine: false
  mock_cycling74_docs: false
```

Create `config/config.development.yaml`:

```yaml
# Development-specific overrides
server:
  debug: true
  port: 8001

logging:
  level: "DEBUG"
  console_output: true
  
development:
  auto_reload: true
  profiling_enabled: true
  debug_knowledge_engine: true
  
cache:
  directory: "./cache/dev"
  
knowledge_sources:
  cycling74_docs:
    cache_duration: 600  # 10 minutes for faster development
    
  minutiae_repo:
    update_interval: 60  # 1 minute for faster updates
```

### 3. Makefile for Development Workflow

Create `Makefile`:

```makefile
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
```

### 4. Pre-commit Configuration

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        additional_dependencies: [flake8-docstrings]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

---

## Git Configuration

### 1. Create .gitignore

Create `.gitignore`:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
.conda/

# IDE
.vscode/settings.json
.idea/
*.swp
*.swo
*~

# Jupyter Notebook
.ipynb_checkpoints

# pytest
.pytest_cache/
.coverage
htmlcov/

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Logs
logs/
*.log

# Cache
cache/
.cache/

# Configuration overrides (keep templates)
config/config.local.yaml
config/config.production.yaml
config/.env

# macOS
.DS_Store
.AppleDouble
.LSOverride

# Documentation builds
docs/_build/
docs/build/

# Temporary files
tmp/
temp/
*.tmp
*.temp

# Database files
*.db
*.sqlite

# Environment variables
.env.local
.env.development
.env.production

# Profiling data
*.prof

# Coverage reports
coverage.xml
*.cover
.hypothesis/

# Backup files
*.bak
*.backup
```

### 2. Git Hooks Setup

Create `.githooks/pre-commit`:

```bash
#!/bin/bash
# Pre-commit hook for intelligent-max-mcp

echo "Running pre-commit checks..."

# Activate conda environment
source ~/anaconda3/etc/profile.d/conda.sh
conda activate intelligent-max-mcp

# Run formatting
echo "Formatting code..."
black src/ tests/
isort src/ tests/

# Run linting
echo "Running linting..."
flake8 src/ tests/
if [ $? -ne 0 ]; then
    echo "Linting failed. Please fix the issues before committing."
    exit 1
fi

# Run type checking
echo "Running type checking..."
mypy src/
if [ $? -ne 0 ]; then
    echo "Type checking failed. Please fix the issues before committing."
    exit 1
fi

# Run tests
echo "Running tests..."
pytest tests/ -q
if [ $? -ne 0 ]; then
    echo "Tests failed. Please fix the issues before committing."
    exit 1
fi

echo "All pre-commit checks passed!"
```

Make it executable:
```bash
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
```

---

## Development Workflow

### 1. Daily Development Commands

```bash
# Start development session
cdmcp  # Custom alias to cd and activate environment

# Pull latest changes
git pull origin main

# Install/update dependencies
make install-dev

# Start development server
make run

# Or debug mode
make debug
```

### 2. Code Quality Workflow

```bash
# Format code
make format

# Check types
make type-check

# Run linting
make lint

# Run tests
make test

# Run tests with coverage
make test-cov

# All checks at once
make check-all
```

### 3. Testing Commands

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_knowledge_engine.py -v

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html

# Run tests and generate coverage report
make test-cov
open htmlcov/index.html  # View coverage in browser
```

---

## Testing Setup

### 1. Pytest Configuration

Create `pytest.ini`:

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --disable-warnings
    --tb=short
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow tests
    knowledge: Knowledge engine tests
    generation: Patcher generation tests
    api: API tests
```

### 2. Test Configuration

Create `tests/conftest.py`:

```python
"""
Pytest configuration and fixtures for intelligent-max-mcp tests
"""
import pytest
import asyncio
from pathlib import Path
import tempfile
import shutil
from unittest.mock import Mock, AsyncMock

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "fixtures"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_cycling74_connector():
    """Mock Cycling '74 documentation connector."""
    mock = AsyncMock()
    mock.search_object.return_value = {
        "object_name": "metro",
        "description": "Metronome object",
        "inlets": [{"index": 0, "type": "int", "description": "Interval"}],
        "outlets": [{"index": 0, "type": "bang", "description": "Bang output"}]
    }
    return mock

@pytest.fixture
def mock_minutiae_connector():
    """Mock minutiae repository connector."""
    mock = AsyncMock()
    mock.search_patterns.return_value = {
        "query": "temporal scaffolding",
        "results": [
            {
                "pattern_name": "exponential_acceleration",
                "description": "Exponential function for rhythm acceleration",
                "confidence_score": 0.95
            }
        ]
    }
    return mock

@pytest.fixture
def sample_patcher_json():
    """Sample Max patcher JSON for testing."""
    return {
        "patcher": {
            "fileversion": 1,
            "appversion": {"major": 8, "minor": 6, "revision": 4},
            "rect": [100, 100, 800, 600],
            "bglocked": 0,
            "openinpresentation": 0,
            "boxes": [
                {
                    "box": {
                        "id": "obj-1",
                        "maxclass": "newobj",
                        "text": "metro 1000",
                        "patching_rect": [100, 100, 80, 22]
                    }
                }
            ],
            "lines": []
        }
    }
```

### 3. Sample Test Files

Create `tests/unit/test_knowledge_engine.py`:

```python
"""
Unit tests for knowledge engine
"""
import pytest
from unittest.mock import AsyncMock, patch
from src.knowledge.engine import KnowledgeEngine

class TestKnowledgeEngine:
    """Test cases for KnowledgeEngine class."""
    
    @pytest.fixture
    def knowledge_engine(self, mock_cycling74_connector, mock_minutiae_connector):
        """Create knowledge engine with mocked connectors."""
        engine = KnowledgeEngine()
        engine.cycling74_connector = mock_cycling74_connector
        engine.minutiae_connector = mock_minutiae_connector
        return engine
    
    @pytest.mark.asyncio
    async def test_search_object_documentation(self, knowledge_engine):
        """Test searching for object documentation."""
        result = await knowledge_engine.search_object("metro")
        
        assert result["object_name"] == "metro"
        assert "description" in result
        assert "inlets" in result
        assert "outlets" in result
    
    @pytest.mark.asyncio
    async def test_search_patterns(self, knowledge_engine):
        """Test searching for patterns in minutiae."""
        result = await knowledge_engine.search_patterns("temporal scaffolding")
        
        assert result["query"] == "temporal scaffolding"
        assert len(result["results"]) > 0
        assert result["results"][0]["confidence_score"] > 0.8
    
    def test_validate_pattern(self, knowledge_engine):
        """Test pattern validation."""
        valid_pattern = {
            "pattern_name": "test_pattern",
            "description": "Test pattern",
            "examples": ["example1"],
            "metadata": {"complexity": "low"}
        }
        
        is_valid = knowledge_engine.validate_pattern(valid_pattern)
        assert is_valid is True
    
    def test_validate_invalid_pattern(self, knowledge_engine):
        """Test validation of invalid pattern."""
        invalid_pattern = {
            "pattern_name": "test_pattern"
            # Missing required fields
        }
        
        is_valid = knowledge_engine.validate_pattern(invalid_pattern)
        assert is_valid is False
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Conda Environment Issues

**Problem**: `conda: command not found`
```bash
# Solution: Add conda to PATH
export PATH="/usr/local/anaconda3/bin:$PATH"
source ~/.zshrc
```

**Problem**: Environment activation fails
```bash
# Solution: Initialize conda properly
conda init zsh  # or bash
source ~/.zshrc
```

#### 2. Python Import Issues

**Problem**: `ModuleNotFoundError` when running tests or scripts
```bash
# Solution: Set PYTHONPATH
export PYTHONPATH="${PWD}/src:$PYTHONPATH"

# Or add to VS Code settings (already included above)
```

#### 3. VS Code Python Interpreter Issues

**Problem**: VS Code not using correct Python interpreter

**Solution**:
1. Open Command Palette (`Cmd+Shift+P`)
2. Type "Python: Select Interpreter"
3. Choose: `~/anaconda3/envs/intelligent-max-mcp/bin/python`

#### 4. Package Installation Issues

**Problem**: Package conflicts or installation failures
```bash
# Solution: Clean and reinstall
conda deactivate
conda env remove -n intelligent-max-mcp
conda create -n intelligent-max-mcp python=3.11
conda activate intelligent-max-mcp
pip install -r requirements.txt
```

#### 5. Permission Issues on macOS

**Problem**: Permission denied errors
```bash
# Solution: Fix permissions
sudo chown -R $(whoami) /usr/local/anaconda3
```

#### 6. Git Hooks Not Working

**Problem**: Pre-commit hooks not running
```bash
# Solution: Make hooks executable and set path
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
```

#### 7. Memory Issues on 8GB MacBook Air

**Problem**: Development environment using too much memory

**Solutions**:
- Close unnecessary applications
- Use lightweight terminals
- Limit concurrent processes:
  ```bash
  # Reduce pytest workers
  pytest tests/ -n 1
  
  # Reduce VS Code extensions
  # Disable heavy extensions when not needed
  ```

### Performance Optimization for 8GB RAM

```bash
# Optimize conda environment
conda config --set auto_activate_base false

# Use lighter alternatives
pip install ipdb  # Instead of full IPython for debugging

# Monitor memory usage
top -o MEM  # Monitor memory usage
htop        # If installed: brew install htop
```

### Environment Variables

Create `.env.example`:
```bash
# Example environment variables
PYTHONPATH=./src
ENVIRONMENT=development
LOG_LEVEL=DEBUG
CACHE_DIR=./cache/dev
```

---

## Verification Checklist

After completing setup, verify everything works:

```bash
# ✅ Check conda environment
conda activate intelligent-max-mcp
python --version  # Should show Python 3.11.x

# ✅ Check package installation
python -c "import mcp; print('MCP OK')"
python -c "import requests; print('Requests OK')"
python -c "import numpy; print('NumPy OK')"

# ✅ Check project structure
tree . -I '__pycache__|*.pyc|.git' -L 3

# ✅ Check VS Code configuration
code .  # Should open with correct interpreter

# ✅ Check development tools
black --version
mypy --version
pytest --version

# ✅ Run basic tests
pytest tests/ -v  # When tests are created

# ✅ Check pre-commit
pre-commit run --all-files

# ✅ Check development server (when implemented)
make run
```

---

## Quick Reference

### Essential Commands
```bash
# Environment
conda activate intelligent-max-mcp
cdmcp  # Custom alias

# Development
make install-dev
make run
make debug
make test
make check-all

# Code Quality
make format
make lint
make type-check

# Git Workflow
git add .
git commit -m "message"  # Pre-commit hooks run automatically
git push origin main
```

### Key Directories
```
src/                 - Source code
tests/               - Test files
config/              - Configuration files
docs/                - Documentation
examples/            - Example code
logs/                - Log files
cache/               - Cache directory
```

### Important Files
```
setup.py             - Package configuration
requirements.txt     - Python dependencies
config/config.yaml   - Main configuration
.vscode/settings.json - VS Code settings
Makefile             - Development commands
```

---

**Environment Setup Complete!** 🎉

You now have a comprehensive development environment ready for building the Intelligent Max MCP Server. Every tool, configuration, and workflow is in place for efficient development and easy reproduction on future machines.
