# 🚀 Setup Guide - Credit Risk Assessment AI

## 📁 Project Structure

```
credit-risk-assessment-ai/
├── backend/          # FastAPI + LangGraph + 6 AI Agents
├── frontend/         # React + Vite + TailwindCSS
├── scripts/          # Startup scripts
├── examples/         # Sample loan applications
└── docker-compose.yml
```

---

## ⚡ Quick Start

### 1. Install UV (Recommended)

```powershell
# PowerShell
irm https://astral.sh/uv/install.ps1 | iex
```

### 2. Configure Environment

```bash
# Copy and edit .env
copy .env.example .env
# Add your OPENAI_API_KEY
```

### 3. Start Everything

```bash
# Option A: Start both services (opens 2 windows)
scripts\start-all.bat

# Option B: Docker Compose
docker-compose up --build
```

---

## 🌐 Access

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:3000 |
| **Backend API** | http://localhost:8080 |
| **API Docs** | http://localhost:8080/docs |

---

## 🛠 Development

### Backend Only

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

### Frontend Only

```bash
cd frontend
npm install
npm run dev
```

---

## 📦 What's Included

### Backend (Python)
- ✅ FastAPI REST API
- ✅ 6 specialized AI agents
- ✅ LangGraph orchestration
- ✅ LangSmith tracing
- ✅ Pydantic models
- ✅ Structured logging

### Frontend (React)
- ✅ Multi-step form
- ✅ Results dashboard
- ✅ Charts (Recharts)
- ✅ TailwindCSS styling
- ✅ Sample data loading
- ✅ Real-time progress

---

## 🔑 Required

- **OPENAI_API_KEY** (required)
- **LANGSMITH_API_KEY** (optional)

---

## 📝 Next Steps

1. Open http://localhost:3000
2. Click "Load Good Profile" or "Load Risky Profile"
3. Submit and see AI analysis
4. View detailed risk assessment

---

**Everything is ready to use!** 🎉
