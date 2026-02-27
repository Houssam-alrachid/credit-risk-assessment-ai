# 🚀 UV Guide - Credit Risk Assessment AI

This guide explains how to use **uv** for fast and efficient Python environment management.

## 📦 What is UV?

[uv](https://docs.astral.sh/uv/) is an extremely fast Python package installer and resolver written in Rust. It's 10-100x faster than pip and provides better dependency resolution.

---

## 🔧 Installation

### Windows (PowerShell)
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

### Linux/macOS
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Alternative (using pip)
```bash
pip install uv
```

---

## 🚀 Quick Start

### 1. Initial Setup
```bash
# Clone the repository
git clone https://github.com/your-repo/credit-risk-assessment-ai.git
cd credit-risk-assessment-ai

# Setup environment (creates .venv and installs dependencies)
scripts\setup-uv.bat

# Or manually
uv sync
```

### 2. Configure Environment
```bash
# Copy environment template
copy .env.example .env

# Edit with your API keys
notepad .env
```

### 3. Run the Application
```bash
# Using script
scripts\run-uv.bat

# Or directly
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

---

## 📚 Common Commands

### Running the Application
```bash
# Development mode with auto-reload
uv run uvicorn app.main:app --reload

# Production mode
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers 4
```

### Running Tests
```bash
# All tests
uv run pytest tests/ -v

# Specific test file
uv run pytest tests/test_models.py -v

# With coverage
uv run pytest tests/ --cov=app --cov=agents --cov-report=html

# Using script
scripts\test-uv.bat
```

### Package Management
```bash
# Add a package
uv add requests
uv add httpx>=0.27.0

# Add dev dependency
uv add --dev pytest
uv add --dev black

# Remove a package
uv remove requests

# Update all packages
uv sync --upgrade

# Update specific package
uv add requests --upgrade

# Using scripts
scripts\add-package.bat requests
scripts\remove-package.bat requests
```

### Environment Management
```bash
# Create/sync environment
uv sync

# Sync with dev dependencies
uv sync --extra dev

# Sync all optional dependencies
uv sync --all-extras

# Remove unused packages
uv sync --prune

# Show installed packages
uv pip list

# Show package info
uv pip show langchain
```

### Lock File Management
```bash
# Generate/update lock file
uv lock

# Sync from lock file
uv sync --locked

# Check for updates
uv lock --upgrade
```

---

## 🎯 UV vs PIP Comparison

| Task | UV | PIP |
|------|-----|-----|
| Install packages | `uv sync` | `pip install -r requirements.txt` |
| Add package | `uv add requests` | `pip install requests` |
| Remove package | `uv remove requests` | `pip uninstall requests` |
| Run script | `uv run python script.py` | `python script.py` |
| Speed | ⚡ 10-100x faster | Standard |
| Lock file | ✅ `uv.lock` | ❌ Manual |

---

## 🔄 Workflow Examples

### Starting Development
```bash
# 1. Setup environment
uv sync

# 2. Activate environment (optional, uv run works without activation)
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 3. Run application
uv run uvicorn app.main:app --reload
```

### Adding a New Feature
```bash
# 1. Add required package
uv add new-package

# 2. Develop feature
# ... code changes ...

# 3. Run tests
uv run pytest tests/ -v

# 4. Lock dependencies
uv lock
```

### Updating Dependencies
```bash
# Update all packages
uv sync --upgrade

# Update specific package
uv add langchain --upgrade

# Check what would be updated
uv lock --upgrade --dry-run
```

---

## 🐳 Docker with UV

The project's Dockerfile uses traditional pip, but you can use uv in Docker:

```dockerfile
FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application
COPY . .

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## 🔍 Troubleshooting

### UV not found
```bash
# Check installation
uv --version

# Reinstall
pip install uv
```

### Dependencies not syncing
```bash
# Force sync
uv sync --reinstall

# Clear cache
uv cache clean
```

### Lock file conflicts
```bash
# Regenerate lock file
rm uv.lock
uv lock
```

### Virtual environment issues
```bash
# Remove and recreate
rm -rf .venv
uv sync
```

---

## 📖 Additional Resources

- [UV Documentation](https://docs.astral.sh/uv/)
- [UV GitHub](https://github.com/astral-sh/uv)
- [UV vs PIP Benchmark](https://github.com/astral-sh/uv#benchmarks)

---

## 💡 Tips & Best Practices

1. **Always use `uv sync`** instead of `pip install` for consistency
2. **Commit `uv.lock`** to version control for reproducible builds
3. **Use `uv run`** to ensure correct environment activation
4. **Add dev dependencies** with `--dev` flag
5. **Update regularly** with `uv sync --upgrade`
6. **Use scripts** in `scripts/` folder for common tasks

---

## 🎓 Learning Path

1. ✅ Install UV
2. ✅ Run `uv sync` to setup environment
3. ✅ Use `uv run` to execute commands
4. ✅ Add packages with `uv add`
5. ✅ Run tests with `uv run pytest`
6. ✅ Update dependencies with `uv sync --upgrade`
7. ✅ Commit `uv.lock` to Git

---

**Ready to go! Use `scripts\run-uv.bat` to start developing.**
