#!/bin/bash
# =============================================================================
# Cloud Run Deployment Script - Credit Risk Assessment AI
# =============================================================================
# This script deploys the application to Google Cloud Run
# =============================================================================

set -e

# =============================================================================
# CONFIGURATION
# =============================================================================
PROJECT_ID="${GCP_PROJECT_ID:-}"
REGION="${GCP_REGION:-europe-west1}"
SERVICE_NAME="credit-risk-api"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "============================================================"
echo "   Cloud Run Deployment - Credit Risk Assessment AI"
echo "============================================================"

# =============================================================================
# VALIDATE CONFIGURATION
# =============================================================================
if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}[ERROR] GCP_PROJECT_ID is not set${NC}"
    echo "Please set it: export GCP_PROJECT_ID=your-project-id"
    exit 1
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${RED}[ERROR] OPENAI_API_KEY is not set${NC}"
    echo "Please set it: export OPENAI_API_KEY=sk-your-key"
    exit 1
fi

echo -e "${GREEN}Configuration:${NC}"
echo "  Project ID: $PROJECT_ID"
echo "  Region: $REGION"
echo "  Service: $SERVICE_NAME"
echo ""

# =============================================================================
# STEP 1: AUTHENTICATE & CONFIGURE
# =============================================================================
echo "============================================================"
echo "[1/6] Configuring GCP project..."
echo "============================================================"

gcloud config set project $PROJECT_ID
echo -e "${GREEN}[OK] Project configured${NC}"

# =============================================================================
# STEP 2: ENABLE REQUIRED APIS
# =============================================================================
echo ""
echo "============================================================"
echo "[2/6] Enabling required APIs..."
echo "============================================================"

gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com

echo -e "${GREEN}[OK] APIs enabled${NC}"

# =============================================================================
# STEP 3: CREATE SECRETS (if using Secret Manager)
# =============================================================================
echo ""
echo "============================================================"
echo "[3/6] Setting up secrets..."
echo "============================================================"

# Check if secret exists, create if not
if ! gcloud secrets describe openai-api-key --project=$PROJECT_ID &>/dev/null; then
    echo "Creating OpenAI API key secret..."
    echo -n "$OPENAI_API_KEY" | gcloud secrets create openai-api-key \
        --replication-policy="automatic" \
        --data-file=-
    echo -e "${GREEN}[OK] Secret created${NC}"
else
    echo -e "${YELLOW}[INFO] Secret already exists${NC}"
fi

# LangSmith secret (optional)
if [ -n "$LANGSMITH_API_KEY" ]; then
    if ! gcloud secrets describe langsmith-api-key --project=$PROJECT_ID &>/dev/null; then
        echo "Creating LangSmith API key secret..."
        echo -n "$LANGSMITH_API_KEY" | gcloud secrets create langsmith-api-key \
            --replication-policy="automatic" \
            --data-file=-
        echo -e "${GREEN}[OK] LangSmith secret created${NC}"
    fi
fi

# =============================================================================
# STEP 4: BUILD DOCKER IMAGE
# =============================================================================
echo ""
echo "============================================================"
echo "[4/6] Building Docker image..."
echo "============================================================"

# Configure Docker for GCR
gcloud auth configure-docker --quiet

# Build image
docker build -t ${IMAGE_NAME}:latest -t ${IMAGE_NAME}:$(git rev-parse --short HEAD 2>/dev/null || echo "v1") .

echo -e "${GREEN}[OK] Image built${NC}"

# =============================================================================
# STEP 5: PUSH IMAGE TO GCR
# =============================================================================
echo ""
echo "============================================================"
echo "[5/6] Pushing image to Container Registry..."
echo "============================================================"

docker push ${IMAGE_NAME}:latest
docker push ${IMAGE_NAME}:$(git rev-parse --short HEAD 2>/dev/null || echo "v1")

echo -e "${GREEN}[OK] Image pushed${NC}"

# =============================================================================
# STEP 6: DEPLOY TO CLOUD RUN
# =============================================================================
echo ""
echo "============================================================"
echo "[6/6] Deploying to Cloud Run..."
echo "============================================================"

# Build secrets argument
SECRETS_ARG="OPENAI_API_KEY=openai-api-key:latest"
if [ -n "$LANGSMITH_API_KEY" ]; then
    SECRETS_ARG="${SECRETS_ARG},LANGSMITH_API_KEY=langsmith-api-key:latest"
fi

gcloud run deploy $SERVICE_NAME \
    --image ${IMAGE_NAME}:latest \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --min-instances 0 \
    --max-instances 10 \
    --set-secrets $SECRETS_ARG \
    --set-env-vars "OPENAI_MODEL=gpt-4o,LANGSMITH_PROJECT=credit-risk-assessment,LANGSMITH_TRACING_ENABLED=true,LOG_LEVEL=INFO,LOG_FORMAT=json"

echo -e "${GREEN}[OK] Deployment complete!${NC}"

# =============================================================================
# GET SERVICE URL
# =============================================================================
echo ""
echo "============================================================"
echo "   Deployment Summary"
echo "============================================================"

SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')

echo ""
echo -e "${GREEN}Your application is deployed!${NC}"
echo ""
echo "  Service URL:  $SERVICE_URL"
echo "  API Docs:     $SERVICE_URL/docs"
echo "  Health Check: $SERVICE_URL/health"
echo ""
echo "============================================================"
echo "   Useful Commands"
echo "============================================================"
echo ""
echo "View logs:"
echo "  gcloud run services logs read $SERVICE_NAME --region $REGION"
echo ""
echo "Update deployment:"
echo "  ./scripts/deploy-cloud-run.sh"
echo ""
echo "Delete service:"
echo "  gcloud run services delete $SERVICE_NAME --region $REGION"
echo ""
