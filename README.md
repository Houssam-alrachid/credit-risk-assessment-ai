# 🏦 Credit Risk Assessment AI

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/React-18-61dafb.svg)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2-orange.svg)](https://github.com/langchain-ai/langgraph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Multi-agent AI system for automated loan underwriting and credit risk assessment.**

Built with LangGraph for orchestration, LangSmith for observability, **React frontend**, and deployed on Google Cloud Run.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [API Reference](#-api-reference)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Overview

This system automates the credit risk assessment process using 6 specialized AI agents:

| Agent                              | Role                                        |
| ---------------------------------- | ------------------------------------------- |
| **Financial Data Collector** | Validates and organizes financial data      |
| **Income Analyzer**          | Assesses income stability and affordability |
| **Debt Analyzer**            | Calculates DTI, DSCR, and debt burden       |
| **Collateral Evaluator**     | Evaluates collateral quality and LTV        |
| **Risk Scorer**              | Computes PD, LGD, and risk classification   |
| **Decision Writer**          | Generates final credit decision and terms   |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     CREDIT RISK ASSESSMENT SYSTEM                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │   FastAPI    │───▶│  LangGraph   │───▶│  LangSmith   │          │
│  │   Endpoint   │    │ Orchestrator │    │   Tracing    │          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
│                             │                                        │
│         ┌───────────────────┼───────────────────┐                   │
│         ▼                   ▼                   ▼                   │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐             │
│  │  Financial  │    │   Income    │    │    Debt     │ PARALLEL    │
│  │   Data      │    │  Analyzer   │    │  Analyzer   │ ANALYSIS    │
│  │  Collector  │    │             │    │             │             │
│  └─────────────┘    └─────────────┘    └─────────────┘             │
│         │                   │                   │                   │
│         └───────────────────┼───────────────────┘                   │
│                             ▼                                        │
│                    ┌─────────────┐                                   │
│                    │  Collateral │                                   │
│                    │  Evaluator  │                                   │
│                    └─────────────┘                                   │
│                             │                                        │
│                             ▼                                        │
│                    ┌─────────────┐                                   │
│                    │    Risk     │                                   │
│                    │   Scorer    │                                   │
│                    └─────────────┘                                   │
│                             │                                        │
│                             ▼                                        │
│                    ┌─────────────┐                                   │
│                    │  Decision   │                                   │
│                    │   Writer    │                                   │
│                    └─────────────┘                                   │
│                             │                                        │
│                             ▼                                        │
│                    ┌─────────────┐                                   │
│                    │   Credit    │                                   │
│                    │   Report    │                                   │
│                    └─────────────┘                                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### Core Capabilities

- ✅ **Automated Credit Decisioning** - Approve, decline, or flag for manual review
- ✅ **Risk Scoring** - PD/LGD/EL calculations with Basel III compliance
- ✅ **DTI Analysis** - Debt-to-income and affordability assessment
- ✅ **Collateral Evaluation** - LTV and liquidation value estimation
- ✅ **Structured Reports** - Detailed credit memos with recommendations

### Technical Features

- ✅ **LangGraph Orchestration** - Multi-agent workflow management
- ✅ **LangSmith Tracing** - Full observability and debugging
- ✅ **Streaming API** - Real-time progress updates via SSE
- ✅ **Docker Ready** - Optimized multi-stage build
- ✅ **Cloud Run Deployment** - Serverless, auto-scaling
- ✅ **CI/CD Pipeline** - GitHub Actions + Cloud Build

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Docker (optional)
- OpenAI API key
- LangSmith API key (optional but recommended)

### Option 1: Using UV (Recommended)

```bash
# Install uv if not already installed
# PowerShell: irm https://astral.sh/uv/install.ps1 | iex
# Or: pip install uv

# Clone repository
git clone https://github.com/your-repo/credit-risk-assessment-ai.git
cd credit-risk-assessment-ai

# Setup environment with uv
scripts\setup-uv.bat

# Configure environment
copy .env.example .env
# Edit .env with your API keys

# Run the application
scripts\run-uv.bat
```

### Option 2: Using pip

```bash
git clone https://github.com/your-repo/credit-risk-assessment-ai.git
cd credit-risk-assessment-ai

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
copy .env.example .env

# Edit .env with your API keys
notepad .env
```

Required variables:

```env
OPENAI_API_KEY=sk-your-openai-key
LANGSMITH_API_KEY=lsv2-your-langsmith-key  # Optional
```

### 3. Run Locally

```bash
# Using UV (recommended)
scripts\run-uv.bat

# Or using pip
scripts\start-local.bat

# Or manually
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

# Or with uv
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### 4. Test the API

Open http://localhost:8080/docs for Swagger UI.

**Sample Request:**

```bash
curl -X POST http://localhost:8080/api/v1/assess \
  -H "Content-Type: application/json" \
  -d @examples/sample_application.json
```

---

## 📚 API Reference

### Endpoints

| Method   | Endpoint                  | Description                  |
| -------- | ------------------------- | ---------------------------- |
| `GET`  | `/`                     | API information              |
| `GET`  | `/health`               | Health check                 |
| `POST` | `/api/v1/assess`        | Full credit assessment       |
| `POST` | `/api/v1/assess/stream` | Assessment with SSE progress |
| `POST` | `/api/v1/validate`      | Validate application         |
| `GET`  | `/api/v1/config`        | Get configuration            |

### Request Schema

```json
{
  "application": {
    "applicant": {
      "first_name": "Jean",
      "last_name": "Dupont",
      "date_of_birth": "1985-05-15"
    },
    "employment": {
      "employment_type": "employed",
      "employer_name": "Tech Corp",
      "years_employed": 5.0,
      "monthly_gross_income": 6000.0,
      "monthly_net_income": 4500.0
    },
    "loan_request": {
      "loan_purpose": "mortgage",
      "requested_amount": 250000.0,
      "requested_term_months": 240
    },
    "credit_history": {
      "credit_score": 720,
      "accounts_open": 5,
      "oldest_account_years": 12.0
    }
  }
}
```

### Response Schema

```json
{
  "success": true,
  "report": {
    "report_id": "uuid",
    "credit_decision": {
      "decision": "approved",
      "confidence_score": 85.0,
      "approved_terms": {
        "approved_amount": 250000.0,
        "interest_rate": 3.5,
        "term_months": 240,
        "monthly_payment": 1449.0
      }
    },
    "risk_assessment": {
      "overall_risk_level": "low",
      "risk_score": 25,
      "probability_of_default": 1.5
    }
  },
  "processing_time_seconds": 12.5,
  "trace_url": "https://smith.langchain.com/..."
}
```

---

## ⚙️ Configuration

### Environment Variables

| Variable              | Required | Default                    | Description               |
| --------------------- | -------- | -------------------------- | ------------------------- |
| `OPENAI_API_KEY`    | ✅       | -                          | OpenAI API key            |
| `OPENAI_MODEL`      | ❌       | `gpt-4o`                 | Model to use              |
| `LANGSMITH_API_KEY` | ❌       | -                          | LangSmith key for tracing |
| `LANGSMITH_PROJECT` | ❌       | `credit-risk-assessment` | Project name              |
| `LOG_LEVEL`         | ❌       | `INFO`                   | Logging level             |
| `MAX_DTI_RATIO`     | ❌       | `0.43`                   | Max debt-to-income ratio  |

---

## 🚢 Deployment

### Docker

```bash
# Build
docker build -t credit-risk-api:latest .

# Run
docker run -p 8080:8080 \
  -e OPENAI_API_KEY=sk-xxx \
  credit-risk-api:latest
```

### Docker Compose

```bash
# Start
docker-compose up --build

# Stop
docker-compose down
```

### Google Cloud Run

#### Option 1: Script Deployment

```bash
# Set environment variables
export GCP_PROJECT_ID=your-project-id
export OPENAI_API_KEY=sk-xxx

# Deploy
./scripts/deploy-cloud-run.sh
```

#### Option 2: Manual Deployment

```bash
# Configure project
gcloud config set project YOUR_PROJECT_ID

# Build and push
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/credit-risk-api

# Deploy
gcloud run deploy credit-risk-api \
  --image gcr.io/YOUR_PROJECT_ID/credit-risk-api \
  --region europe-west1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --set-secrets OPENAI_API_KEY=openai-api-key:latest
```

### CI/CD

The project includes:

- **GitHub Actions** (`.github/workflows/ci-cd.yml`)
- **Cloud Build** (`cloudbuild.yaml`)

Configure secrets in your repository:

- `GCP_PROJECT_ID`
- `GCP_SA_KEY` (Service Account JSON)
- `OPENAI_API_KEY`

---

## 🛠 Development

### Project Structure

```
credit-risk-assessment-ai/
├── backend/                      # FastAPI Backend
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   └── models.py            # Pydantic models
│   ├── agents/                  # 6 specialized AI agents
│   │   ├── base_agent.py
│   │   ├── financial_data_collector.py
│   │   ├── income_analyzer.py
│   │   ├── debt_analyzer.py
│   │   ├── collateral_evaluator.py
│   │   ├── risk_scorer.py
│   │   └── decision_writer.py
│   ├── graphs/
│   │   └── credit_assessment_graph.py  # LangGraph workflow
│   ├── services/
│   │   └── credit_assessment_service.py
│   ├── config/
│   │   ├── settings.py
│   │   └── logging_config.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── requirements.txt
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── ApplicationForm.jsx
│   │   │   ├── ResultsDashboard.jsx
│   │   │   └── LoadingOverlay.jsx
│   │   ├── api/
│   │   │   └── creditApi.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── scripts/
│   ├── start-all.bat            # Start both services
│   ├── start-backend.bat
│   ├── start-frontend.bat
│   └── deploy-cloud-run.sh
├── examples/
│   ├── sample_application.json
│   └── sample_application_risky.json
├── .github/workflows/
│   └── ci-cd.yml
├── docker-compose.yml
├── .env.example
└── README.md
```

### Running Tests

```bash
# Using UV (recommended)
scripts\test-uv.bat

# Or directly
uv run pytest tests/ -v

# With coverage
uv run pytest tests/ -v --cov=app --cov=agents --cov-report=html

# Using pip
pytest tests/ -v
```

### Code Style

```bash
# Install dev dependencies with uv
uv sync --extra dev

# Format
uv run black .
uv run isort .

# Lint
uv run flake8 .
```

### Package Management with UV

```bash
# Add a package
scripts\add-package.bat package-name
# Or: uv add package-name

# Add dev dependency
uv add --dev package-name

# Remove a package
scripts\remove-package.bat package-name
# Or: uv remove package-name

# Update all packages
uv sync --upgrade

# Lock dependencies
uv lock
```

---

## 🔧 Troubleshooting

### Common Issues

**1. OpenAI API Error**

```
Error: AuthenticationError
```

→ Verify `OPENAI_API_KEY` is set correctly

**2. LangSmith Not Tracing**

```
Tracing disabled
```

→ Set `LANGSMITH_API_KEY` and `LANGSMITH_TRACING_ENABLED=true`

**3. Docker Build Fails**

```
Error: pip install failed
```

→ Ensure `requirements.txt` is valid and dependencies are compatible

**4. Cloud Run 503 Error**

```
Service unavailable
```

→ Check logs: `gcloud run services logs read credit-risk-api`

### Logs

```bash
# Local
# Check console output

# Cloud Run
gcloud run services logs read credit-risk-api --region europe-west1

# Docker
docker logs credit-risk-api
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Contact

**Houssam Alrachid** - alrachid.houssam@gmail.com

Project Link: [https://github.com/your-repo/credit-risk-assessment-ai](https://github.com/your-repo/credit-risk-assessment-ai)
