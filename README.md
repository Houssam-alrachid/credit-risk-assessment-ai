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
