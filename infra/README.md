# CivicPulse Engine Infrastructure

This directory contains all infrastructure-as-code and deployment configurations for the CivicPulse Engine.

## Directory Structure

```
infra/
├── docker/                    # Docker configurations
│   ├── Dockerfile.api         # API server image
│   ├── Dockerfile.worker      # Background worker image
│   ├── Dockerfile.frontend    # Frontend React app image
│   └── nginx.conf            # Nginx config for frontend
│
├── aws/                       # AWS-specific configs
│   └── ecs-task-def.json     # ECS Fargate task definition
│
├── k8s/                       # Kubernetes manifests
│   ├── api-deployment.yaml   # API deployment & config
│   ├── worker-deployment.yaml # Worker deployment
│   └── service.yaml          # Services & ingress
│
├── terraform/                 # Terraform IaC
│   └── main.tf               # AWS infrastructure setup
│
├── docker-compose.dev.yml    # Local development overrides
├── deploy.sh                 # Bash deployment script
└── deploy.ps1                # PowerShell deployment script
```

## Quick Start

### Local Development with Docker Compose

1. **Start all services:**
   ```bash
   docker-compose up
   ```

2. **With development hot-reload:**
   ```bash
   docker-compose -f docker-compose.yml -f infra/docker-compose.dev.yml up
   ```

3. **Access the application:**
   - API: http://localhost:8000
   - Frontend: http://localhost:3000
   - Database: localhost:5432

### Building Individual Images

```bash
# API
docker build -f infra/docker/Dockerfile.api -t civicpulse-api:latest .

# Worker
docker build -f infra/docker/Dockerfile.worker -t civicpulse-worker:latest .

# Frontend
docker build -f infra/docker/Dockerfile.frontend -t civicpulse-frontend:latest .
```

## AWS Deployment

### Prerequisites

- AWS CLI configured with appropriate credentials
- Docker installed
- ECR repositories created (or script will create them)

### Deploy to AWS ECS

```bash
# Linux/Mac
./infra/deploy.sh

# Windows PowerShell
.\infra\deploy.ps1
```

### Custom deployment options

```bash
# Specify custom image tag
IMAGE_TAG=v1.2.3 ./infra/deploy.sh

# PowerShell
.\infra\deploy.ps1 -ImageTag "v1.2.3" -AwsRegion "us-west-2"
```

### Manual AWS Setup

1. **Create VPC and networking (using Terraform):**
   ```bash
   cd infra/terraform
   terraform init
   terraform plan
   terraform apply
   ```

2. **Create ECS cluster:**
   ```bash
   aws ecs create-cluster --cluster-name civicpulse-cluster
   ```

3. **Deploy task definition:**
   ```bash
   aws ecs register-task-definition --cli-input-json file://infra/aws/ecs-task-def.json
   ```

4. **Create ECS service:**
   ```bash
   aws ecs create-service \
     --cluster civicpulse-cluster \
     --service-name civicpulse-api-service \
     --task-definition civicpulse-engine \
     --desired-count 2 \
     --launch-type FARGATE
   ```

## Kubernetes Deployment

### Prerequisites

- kubectl configured with cluster access
- Docker images pushed to registry

### Deploy to Kubernetes

1. **Create namespace:**
   ```bash
   kubectl create namespace civicpulse
   ```

2. **Create secrets:**
   ```bash
   kubectl create secret generic civicpulse-secrets \
     --from-literal=database-url="postgresql://user:pass@host:5432/db" \
     --from-literal=openai-api-key="sk-..." \
     --namespace civicpulse
   ```

3. **Deploy applications:**
   ```bash
   kubectl apply -f infra/k8s/ --namespace civicpulse
   ```

4. **Check status:**
   ```bash
   kubectl get pods --namespace civicpulse
   kubectl get services --namespace civicpulse
   ```

## Environment Variables

### Required for all services:

- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - OpenAI API key for LLM classification

### Optional:

- `OPENAI_BASE_URL` - Custom OpenAI-compatible API endpoint
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `ENVIRONMENT` - Environment name (development, staging, production)

## Monitoring & Logging

### Docker Compose Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
```

### AWS CloudWatch Logs

Logs are automatically sent to CloudWatch when using ECS:
- Log group: `/ecs/civicpulse-api`
- Log group: `/ecs/civicpulse-worker`

### Kubernetes Logs

```bash
# View pod logs
kubectl logs -f deployment/civicpulse-api --namespace civicpulse

# View worker logs
kubectl logs -f deployment/civicpulse-worker --namespace civicpulse
```

## Health Checks

All services expose health check endpoints:

- **API**: `GET /health` - Returns 200 if healthy
- **API**: `GET /ready` - Returns 200 if ready to accept traffic

Docker health checks are configured in Dockerfiles and will restart containers if unhealthy.

## Scaling

### Docker Compose

```bash
# Scale workers
docker-compose up --scale worker=3
```

### ECS

```bash
# Update desired count
aws ecs update-service \
  --cluster civicpulse-cluster \
  --service civicpulse-api-service \
  --desired-count 5
```

### Kubernetes

```bash
# Scale API deployment
kubectl scale deployment civicpulse-api --replicas=5 --namespace civicpulse

# Auto-scaling (HPA)
kubectl autoscale deployment civicpulse-api \
  --min=2 --max=10 \
  --cpu-percent=70 \
  --namespace civicpulse
```

## Database Migrations

Run migrations after deployment:

```bash
# Docker Compose
docker-compose exec api python scripts/run_migrations.py

# Kubernetes
kubectl exec -it deployment/civicpulse-api --namespace civicpulse -- python scripts/run_migrations.py
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs api

# Inspect container
docker inspect civicpulse_api_1
```

### Database connection issues

```bash
# Test database connectivity
docker-compose exec api python -c "import psycopg2; print(psycopg2.connect('$DATABASE_URL'))"
```

### ECS deployment fails

```bash
# Check task status
aws ecs describe-tasks --cluster civicpulse-cluster --tasks <task-id>

# View CloudWatch logs
aws logs tail /ecs/civicpulse-api --follow
```

## Security Notes

- Never commit `.env` files with real credentials
- Use AWS Secrets Manager or Parameter Store for production secrets
- Restrict database security groups to only application servers
- Enable encryption at rest for RDS
- Use HTTPS/TLS for all external endpoints
- Regularly rotate credentials and API keys

## Cost Optimization

### Development
- Use `docker-compose.yml` for local development (free)
- Stop containers when not in use

### AWS Production
- Use RDS reserved instances for predictable workloads
- Use Fargate Spot for non-critical worker tasks
- Enable RDS auto-scaling for storage
- Use CloudWatch alarms to track costs
- Consider EC2 instances for high-volume workloads

## Support

For deployment issues, check:
1. Application logs
2. Infrastructure status (ECS, RDS, etc.)
3. Network connectivity (security groups, VPC)
4. Resource limits (CPU, memory, connections)
