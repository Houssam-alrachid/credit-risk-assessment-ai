# Scripts Directory

Essential automation scripts for development and deployment.

---

## 🚀 Development Scripts

### `start-all.bat`
**Start both frontend and backend** in separate terminal windows.
```bash
scripts\start-all.bat
```
- Backend: http://localhost:8080
- Frontend: http://localhost:3000
- **Recommended for local development**

### `start-backend.bat`
**Start backend only** (FastAPI on port 8080).
```bash
scripts\start-backend.bat
```
Use when developing backend features or testing API endpoints.

### `start-frontend.bat`
**Start frontend only** (React on port 3000).
```bash
scripts\start-frontend.bat
```
Use when developing UI features. Requires backend to be running separately.

---

## ☁️ Deployment Script

### `deploy-cloud-run.sh`
Deploy the application to Google Cloud Run (Linux/Mac/WSL).
```bash
./scripts/deploy-cloud-run.sh
```

**Prerequisites:**
- Google Cloud SDK installed (`gcloud`)
- Authenticated to GCP (`gcloud auth login`)
- Project configured (`gcloud config set project PROJECT_ID`)
- Required APIs enabled (Cloud Run, Container Registry, Cloud Build)

**What it does:**
1. Builds Docker images for backend and frontend
2. Pushes images to Google Container Registry
3. Deploys to Cloud Run
4. Runs smoke tests

---

## 📝 Quick Reference

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `start-all.bat` | Start full stack | Daily development |
| `start-backend.bat` | Backend only | API development/testing |
| `start-frontend.bat` | Frontend only | UI development |
| `deploy-cloud-run.sh` | Deploy to GCP | Production deployment |

**Stop Services:**
- Press `Ctrl+C` in each terminal window

---

## 🔧 Package Management

For Python package management, use UV directly:
```bash
# Add package
uv add <package-name>

# Remove package
uv remove <package-name>

# Sync dependencies
uv sync
```

See `UV_GUIDE.md` in the root directory for more details.
