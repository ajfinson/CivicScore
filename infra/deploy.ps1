# PowerShell Deployment Script for CivicPulse Engine

param(
    [string]$AwsRegion = "us-east-1",
    [string]$ImageTag = "latest",
    [string]$Environment = "production"
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting CivicPulse Engine Deployment" -ForegroundColor Green

# Get AWS Account ID
Write-Host "==> Getting AWS Account ID..." -ForegroundColor Blue
$AwsAccountId = (aws sts get-caller-identity --query Account --output text)
$EcrRegistry = "$AwsAccountId.dkr.ecr.$AwsRegion.amazonaws.com"

# Step 1: Build Docker images
Write-Host "==> Building Docker images..." -ForegroundColor Blue
docker build -f infra/docker/Dockerfile.api -t civicpulse-api:$ImageTag .
docker build -f infra/docker/Dockerfile.worker -t civicpulse-worker:$ImageTag .
docker build -f infra/docker/Dockerfile.frontend -t civicpulse-frontend:$ImageTag .

# Step 2: Login to ECR
Write-Host "==> Logging in to AWS ECR..." -ForegroundColor Blue
$LoginPassword = aws ecr get-login-password --region $AwsRegion
$LoginPassword | docker login --username AWS --password-stdin $EcrRegistry

# Step 3: Create ECR repositories if they don't exist
Write-Host "==> Ensuring ECR repositories exist..." -ForegroundColor Blue
$repositories = @("civicpulse-api", "civicpulse-worker", "civicpulse-frontend")

foreach ($repo in $repositories) {
    try {
        aws ecr describe-repositories --repository-names $repo --region $AwsRegion 2>$null
        Write-Host "Repository $repo already exists" -ForegroundColor Gray
    }
    catch {
        Write-Host "Creating repository $repo..." -ForegroundColor Yellow
        aws ecr create-repository --repository-name $repo --region $AwsRegion
    }
}

# Step 4: Tag and push images
Write-Host "==> Pushing images to ECR..." -ForegroundColor Blue
foreach ($service in @("api", "worker", "frontend")) {
    $localTag = "civicpulse-$service`:$ImageTag"
    $remoteTag = "$EcrRegistry/civicpulse-$service`:$ImageTag"
    
    Write-Host "Tagging $localTag -> $remoteTag" -ForegroundColor Gray
    docker tag $localTag $remoteTag
    
    Write-Host "Pushing $remoteTag" -ForegroundColor Gray
    docker push $remoteTag
}

# Step 5: Update ECS service (if using ECS)
Write-Host "==> Updating ECS service..." -ForegroundColor Blue
try {
    aws ecs update-service `
        --cluster civicpulse-cluster `
        --service civicpulse-api-service `
        --force-new-deployment `
        --region $AwsRegion
    Write-Host "ECS service updated successfully" -ForegroundColor Green
}
catch {
    Write-Host "ECS service not found or error updating, skipping..." -ForegroundColor Yellow
}

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Verify deployment in AWS Console"
Write-Host "2. Run database migrations: python scripts/run_migrations.py"
Write-Host "3. Monitor logs in CloudWatch"
