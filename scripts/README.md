# Scripts Directory

## 🚀 Server Management

### `start-all.bat`
**Start both frontend and backend** in separate windows.
```bash
scripts\start-all.bat
```
This is the recommended way to start the application.

### `start-backend.bat`
**Start backend only** (FastAPI on port 8080).
```bash
scripts\start-backend.bat
```

### `start-frontend.bat`
**Start frontend only** (React on port 3000).
```bash
scripts\start-frontend.bat
```

---

## 📦 Package Management

### `add-package.bat`
Add a Python package to the backend using UV.
```bash
scripts\add-package.bat <package-name>
```

### `remove-package.bat`
Remove a Python package from the backend.
```bash
scripts\remove-package.bat <package-name>
```

### `setup-uv.bat`
Install UV package manager.
```bash
scripts\setup-uv.bat
```

---

## ☁️ Deployment

### `deploy-cloud-run.bat` / `deploy-cloud-run.sh`
Deploy the application to Google Cloud Run.
```bash
# Windows
scripts\deploy-cloud-run.bat

# Linux/Mac
./scripts/deploy-cloud-run.sh
```

---

## 📝 Usage Summary

**Most Common:**
- `start-all.bat` - Start everything
- `start-backend.bat` - Backend only
- `start-frontend.bat` - Frontend only

**Stop Services:**
- Press `Ctrl+C` in each terminal window
