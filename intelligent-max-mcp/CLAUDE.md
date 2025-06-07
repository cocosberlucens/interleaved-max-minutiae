# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Intelligent Max MCP Server is a Model Context Protocol (MCP) server that provides intelligent Max/MSP documentation access and patcher generation capabilities. It integrates official Cycling '74 documentation with the `interleaved-max-minutiae` knowledge base to offer context-aware assistance for Max/MSP development.

## Development Commands

### Environment Setup
```bash
# Create conda environment
make env-create

# Install with development dependencies
make install-dev

# One-command development setup
make dev-setup
```

### Core Development Tasks
```bash
# Run the MCP server
make run
# Or directly: python src/main.py --config config/config.development.yaml

# Run tests
make test

# Run tests with coverage
make test-cov

# Format code (black + isort)
make format

# Run linting
make lint

# Type checking
make type-check

# All checks before commit
make check-all
```

### Testing
```bash
# Run specific test file
pytest tests/unit/test_knowledge_engine.py -v

# Run specific test
pytest tests/unit/test_knowledge_engine.py::TestKnowledgeEngine::test_query_docs -v

# Run with debugging
pytest -s tests/unit/test_knowledge_engine.py
```

## Architecture

### Core Components

1. **MCP Server** (`src/core/mcp_server.py`)
   - Handles MCP protocol communication
   - Routes requests to appropriate handlers
   - Manages server lifecycle

2. **Knowledge Engine** (`src/knowledge/engine.py`)
   - Integrates multiple knowledge sources
   - Provides unified query interface
   - Manages caching and updates

3. **Patcher Generator** (`src/generation/patcher_generator.py`)
   - Creates Max patcher JSON structures
   - Applies templates and patterns
   - Validates generated patches

4. **API Functions** (`src/api/functions.py`)
   - Implements MCP function definitions
   - Handles parameter validation
   - Returns structured responses

### Knowledge Sources

1. **Cycling '74 Connector** (`src/knowledge/cycling74_connector.py`)
   - Fetches official documentation
   - Caches responses
   - Handles rate limiting

2. **Minutiae Connector** (`src/knowledge/minutiae_connector.py`)
   - Accesses local knowledge repository
   - Indexes patterns and discoveries
   - Watches for updates

### Key Integrations

- **Parent Repository**: The server runs within `interleaved-max-minutiae` and accesses its knowledge base at `../`
- **Configuration**: Uses YAML configs in `config/` with environment-specific overrides
- **Caching**: Local cache in `cache/` directory for performance
- **Logging**: Structured logs in `logs/` with rotation

## Development Workflow

### Pre-commit Hooks
The repository uses a unified git hooks system at `../.git-hooks/pre-commit` that:
- Formats Python code with black/isort
- Runs flake8 linting
- Performs mypy type checking
- Runs tests when Python files change
- Checks for large files and merge conflicts

### Configuration
- Main config: `config/config.yaml`
- Development overrides: `config/config.development.yaml`
- Testing config: `config/config.testing.yaml`

### MCP Protocol Implementation
The server implements these core MCP functions:
- `max_query_docs()` - Query Cycling '74 documentation
- `max_query_minutiae()` - Search knowledge base
- `max_create_patcher()` - Generate Max patches
- `max_analyze_patcher()` - Analyze existing patches
- `max_create_temporal_scaffolding()` - Generate temporal systems
- `max_enhance_knowledge()` - Add discoveries to knowledge base

## Important Considerations

### Knowledge Base Access
- The server expects the minutiae repository at `../` relative to the project root
- It watches for changes and auto-updates its index
- New discoveries can be automatically integrated

### Cycling '74 Documentation
- Uses legacy Max 8 docs at `https://docs.cycling74.com/legacy/max8`
- Implements caching and retry logic
- Respects rate limits

### Pattern Recognition
- Confidence threshold of 0.8 for accepting new patterns
- Automatic validation before knowledge base integration
- Continuous learning from user interactions

### Testing Strategy
- Unit tests for individual components
- Integration tests for knowledge source connections
- Mock external dependencies in tests
- Use fixtures in `tests/fixtures/` for test data