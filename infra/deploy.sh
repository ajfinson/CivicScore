#!/bin/bash
# Deployment script for CivicPulse Engine

set -e

echo "🚀 Starting CivicPulse Engine Deployment"

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
IMAGE_TAG=${IMAGE_TAG:-latest}

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}==>${NC} ${GREEN}$1${NC}"
}

# Step 1: Build Docker images
print_step "Building Docker images..."
docker build -f infra/docker/Dockerfile.api -t civicpulse-api:${IMAGE_TAG} .
docker build -f infra/docker/Dockerfile.worker -t civicpulse-worker:${IMAGE_TAG} .
docker build -f infra/docker/Dockerfile.frontend -t civicpulse-frontend:${IMAGE_TAG} .

# Step 2: Login to ECR
print_step "Logging in to AWS ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}

# Step 3: Create ECR repositories if they don't exist
print_step "Creating ECR repositories..."
for repo in civicpulse-api civicpulse-worker civicpulse-frontend; do
    aws ecr describe-repositories --repository-names ${repo} --region ${AWS_REGION} 2>/dev/null || \
    aws ecr create-repository --repository-name ${repo} --region ${AWS_REGION}
done

# Step 4: Tag and push images
print_step "Pushing images to ECR..."
for service in api worker frontend; do
    docker tag civicpulse-${service}:${IMAGE_TAG} ${ECR_REGISTRY}/civicpulse-${service}:${IMAGE_TAG}
    docker push ${ECR_REGISTRY}/civicpulse-${service}:${IMAGE_TAG}
done

# Step 5: Update ECS service (if using ECS)
print_step "Updating ECS service..."
aws ecs update-service \
    --cluster civicpulse-cluster \
    --service civicpulse-api-service \
    --force-new-deployment \
    --region ${AWS_REGION} || echo "ECS service not found, skipping..."

print_step "Deployment complete! ✅"
