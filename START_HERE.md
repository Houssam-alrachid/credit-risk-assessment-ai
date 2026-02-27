# 🚀 START HERE - Credit Risk Assessment AI

## ⚠️ IMPORTANT: Project Structure Changed

Le projet a été réorganisé en **frontend/** et **backend/** séparés.

**N'utilisez PLUS les anciens scripts !**

---

## ✅ Comment Démarrer

### Option 1: Tout Démarrer (Recommandé)

```bash
scripts\start-all.bat
```

Cela ouvre **2 fenêtres** :
- Backend API sur http://localhost:8080
- Frontend React sur http://localhost:3000

### Option 2: Démarrer Séparément

**Terminal 1 - Backend:**
```bash
scripts\start-backend.bat
```

**Terminal 2 - Frontend:**
```bash
scripts\start-frontend.bat
```

### Option 3: Docker Compose

```bash
docker-compose up --build
```

---

## 🌐 URLs d'Accès

| Service | URL |
|---------|-----|
| **Frontend (Interface Web)** | http://localhost:3000 |
| **Backend API** | http://localhost:8080 |
| **API Docs (Swagger)** | http://localhost:8080/docs |

---

## 📋 Prérequis

1. **Clé OpenAI** configurée dans `.env`:
   ```
   OPENAI_API_KEY=sk-votre-cle
   ```

2. **UV installé** (pour backend):
   ```powershell
   irm https://astral.sh/uv/install.ps1 | iex
   ```

3. **Node.js installé** (pour frontend):
   - Télécharger sur https://nodejs.org/

---

## 🎯 Première Utilisation

1. **Installer les dépendances frontend:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

2. **Lancer tout:**
   ```bash
   scripts\start-all.bat
   ```

3. **Ouvrir le navigateur:**
   - http://localhost:3000

4. **Tester avec les profils pré-chargés:**
   - Cliquez sur "Load Good Profile (Marie)"
   - Ou "Load Risky Profile (Pierre)"
   - Soumettez le formulaire

---

## 🛑 Arrêter les Services

- **Ctrl+C** dans chaque fenêtre de terminal
- Ou utilisez `scripts\stop-server.bat`

---

## ❌ Scripts Dépréciés (Ne Plus Utiliser)

- ~~`scripts\run-uv.bat`~~ → Utilisez `scripts\start-backend.bat`
- ~~`scripts\start-local.bat`~~ → Utilisez `scripts\start-all.bat`

---

**Tout est prêt ! Lancez `scripts\start-all.bat` pour commencer.** 🎉
