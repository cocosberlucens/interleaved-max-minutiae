# Git Hooks System - Unified Setup

## Overview

This repository uses a **unified git hooks system** that handles both:
- **General repository checks** (for all file changes)
- **MCP-specific Python checks** (only when `intelligent-max-mcp/` files are modified)

## How It Works

### Intelligent Hook Detection
The unified `pre-commit` hook automatically detects which type of changes you're committing:

```bash
# General checks (always run):
✅ Large file detection
✅ Merge conflict markers check
✅ Basic file validation

# MCP-specific checks (only when Python files in intelligent-max-mcp/ are changed):
🐍 Conda environment activation
🔧 Black code formatting
📋 isort import sorting
🔍 flake8 linting
🔎 mypy type checking
🧪 pytest test execution
```

### Setup Commands

```bash
# Make sure hooks are executable and active
chmod +x .git-hooks/pre-commit
chmod +x .git-hooks/post-commit-corrado
git config core.hooksPath .git-hooks
```

### Directory Structure

```
.git-hooks/                          # Main hooks directory
├── pre-commit                       # ✅ Unified pre-commit (NEW)
├── post-commit-corrado              # ✅ Knowledge base generation (EXISTING)
├── post-commit-template
├── generate_knowledge_index.py
└── README.md

intelligent-max-mcp/                 # MCP project directory
├── .pre-commit-config.yaml          # Pre-commit tool config (optional)
└── (no .git-hooks directory)        # ✅ Removed to avoid conflicts
```

## Workflow Examples

### Working on MCP Project Files
```bash
# Edit Python files in intelligent-max-mcp/
vim intelligent-max-mcp/src/knowledge/engine.py

# Stage changes
git add intelligent-max-mcp/src/knowledge/engine.py

# Commit triggers:
# 1. General repository checks
# 2. MCP-specific Python checks (formatting, linting, tests)
git commit -m "Add knowledge engine implementation"
```

### Working on Other Repository Files
```bash
# Edit documentation
vim jsui-temporal-scaffolding/README.md

# Stage changes
git add jsui-temporal-scaffolding/README.md

# Commit triggers:
# 1. General repository checks only
# 2. Post-commit knowledge base regeneration
git commit -m "Update temporal scaffolding docs"
```

## Benefits

1. **No Hook Conflicts** - Single `core.hooksPath` setting
2. **Intelligent Execution** - Only runs relevant checks
3. **Performance** - Skips Python checks for non-Python changes
4. **Backwards Compatible** - Existing post-commit hooks still work
5. **Environment Aware** - Gracefully handles missing tools/environments

## Troubleshooting

### If hooks don't run:
```bash
# Check hook path setting
git config core.hooksPath
# Should show: .git-hooks

# Check hook permissions
ls -la .git-hooks/
# pre-commit and post-commit-corrado should be executable

# Fix permissions if needed
chmod +x .git-hooks/*
```

### If conda environment not found:
```bash
# The hook will warn but continue with system Python
# To fix: create the environment
conda create -n intelligent-max-mcp python=3.11
```

### If Python tools not found:
```bash
# Install development tools
pip install black isort flake8 mypy pytest
```

---

*This unified system ensures smooth development workflow while maintaining code quality across all parts of the repository.*
