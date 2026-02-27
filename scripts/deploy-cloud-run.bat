@echo off
REM =============================================================================
REM Cloud Run Deployment Script - Credit Risk Assessment AI (Windows)
REM =============================================================================

echo ============================================================
echo    Cloud Run Deployment - Credit Risk Assessment AI
echo ============================================================
echo.

REM =============================================================================
REM CONFIGURATION
REM =============================================================================
if "%GCP_PROJECT_ID%"=="" (
    set /p GCP_PROJECT_ID="Enter your GCP Project ID: "
)
if "%GCP_REGION%"=="" (
    set GCP_REGION=europe-west1
)
set SERVICE_NAME=credit-risk-api
set IMAGE_NAME=gcr.io/%GCP_PROJECT_ID%/%SERVICE_NAME%

echo Configuration:
echo   Project ID: %GCP_PROJECT_ID%
echo   Region: %GCP_REGION%
echo   Service: %SERVICE_NAME%
echo.

REM =============================================================================
REM VALIDATE API KEYS
REM =============================================================================
if "%OPENAI_API_KEY%"=="" (
    set /p OPENAI_API_KEY="Enter your OPENAI_API_KEY: "
)
if "%OPENAI_API_KEY%"=="" (
    echo [ERROR] OPENAI_API_KEY is required
    pause
    exit /b 1
)

set /p LANGSMITH_API_KEY="Enter your LANGSMITH_API_KEY (optional, press Enter to skip): "

REM =============================================================================
REM STEP 1: CONFIGURE PROJECT
REM =============================================================================
echo ============================================================
echo [1/6] Configuring GCP project...
echo ============================================================

call gcloud config set project %GCP_PROJECT_ID%
if %errorlevel% neq 0 (
    echo [ERROR] Failed to configure project
    pause
    exit /b 1
)
echo [OK] Project configured
echo.

REM =============================================================================
REM STEP 2: ENABLE APIS
REM =============================================================================
echo ============================================================
echo [2/6] Enabling required APIs...
echo ============================================================

call gcloud services enable run.googleapis.com
call gcloud services enable containerregistry.googleapis.com
call gcloud services enable secretmanager.googleapis.com
echo [OK] APIs enabled
echo.

REM =============================================================================
REM STEP 3: CONFIGURE DOCKER
REM =============================================================================
echo ============================================================
echo [3/6] Configuring Docker for GCR...
echo ============================================================

call gcloud auth configure-docker --quiet
echo [OK] Docker configured
echo.

REM =============================================================================
REM STEP 4: BUILD IMAGE
REM =============================================================================
echo ============================================================
echo [4/6] Building Docker image...
echo ============================================================

docker build -t %IMAGE_NAME%:latest .
if %errorlevel% neq 0 (
    echo [ERROR] Docker build failed
    pause
    exit /b 1
)
echo [OK] Image built
echo.

REM =============================================================================
REM STEP 5: PUSH IMAGE
REM =============================================================================
echo ============================================================
echo [5/6] Pushing image to Container Registry...
echo ============================================================

docker push %IMAGE_NAME%:latest
if %errorlevel% neq 0 (
    echo [ERROR] Docker push failed
    pause
    exit /b 1
)
echo [OK] Image pushed
echo.

REM =============================================================================
REM STEP 6: DEPLOY TO CLOUD RUN
REM =============================================================================
echo ============================================================
echo [6/6] Deploying to Cloud Run...
echo ============================================================

REM Build environment variables
set ENV_VARS=OPENAI_API_KEY=%OPENAI_API_KEY%,OPENAI_MODEL=gpt-4o,LANGSMITH_PROJECT=credit-risk-assessment,LOG_LEVEL=INFO

if not "%LANGSMITH_API_KEY%"=="" (
    set ENV_VARS=%ENV_VARS%,LANGSMITH_API_KEY=%LANGSMITH_API_KEY%,LANGSMITH_TRACING_ENABLED=true
)

call gcloud run deploy %SERVICE_NAME% ^
    --image %IMAGE_NAME%:latest ^
    --platform managed ^
    --region %GCP_REGION% ^
    --allow-unauthenticated ^
    --port 8080 ^
    --memory 2Gi ^
    --cpu 2 ^
    --timeout 300 ^
    --min-instances 0 ^
    --max-instances 10 ^
    --set-env-vars "%ENV_VARS%"

if %errorlevel% neq 0 (
    echo [ERROR] Deployment failed
    pause
    exit /b 1
)

echo [OK] Deployment complete!
echo.

REM =============================================================================
REM GET SERVICE URL
REM =============================================================================
echo ============================================================
echo    Deployment Summary
echo ============================================================
echo.

for /f "tokens=*" %%i in ('gcloud run services describe %SERVICE_NAME% --region %GCP_REGION% --format "value(status.url)"') do set SERVICE_URL=%%i

echo Your application is deployed!
echo.
echo   Service URL:  %SERVICE_URL%
echo   API Docs:     %SERVICE_URL%/docs
echo   Health Check: %SERVICE_URL%/health
echo.
echo ============================================================
echo.
pause
