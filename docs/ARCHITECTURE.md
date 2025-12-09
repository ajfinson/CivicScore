# CivicPulse Engine Architecture

## Overview

CivicPulse Engine is a multi-tenant incident management platform designed to ingest, classify, track, and analyze citizen or customer issue reports. The system is built with a focus on high-volume data processing, SQL optimization, Python concurrency patterns, and cloud deployment.

## System Architecture

### High-Level Components

```
┌─────────────────────────────────────────────────────────────┐
│                         Users Layer                          │
│              (Residents, Tenants, Staff)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway (FastAPI)                    │
│  - Report Ingestion   - Query API   - Dashboard API         │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   Ingestion      Query/Read     Score APIs
   Service         Endpoints
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│            Background Processing Workers                     │
│  - Deduplication Worker (ThreadPool)                        │
│  - SLA Calculator (ThreadPool)                              │
│  - Score Aggregator (ProcessPool)                           │
│  - Scheduler (Job Coordinator)                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   Core Analytics Engine                      │
│  - Issue Grouping & Deduplication                           │
│  - SLA Computations & Tracking                              │
│  - Trend Metrics & Rankings                                 │
│  - Multi-tenant Rule Evaluation                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              PostgreSQL Database (AWS RDS)                   │
│           Multi-tenant Relational Data Store                 │
│  Tables: tenants, areas, issues, reports,                   │
│          sla_metrics, performance_scores                     │
└─────────────────────────────────────────────────────────────┘

        ┌──────────────────────────────┐
        │   LLM Classification Layer   │
        │   - Category Inference       │
        │   - Severity Detection       │
        │   - Similarity Matching      │
        └──────────────────────────────┘
```

## Core Data Flow

### 1. Report Ingestion Flow

```
User Submits Report
    │
    ▼
POST /reports/ (FastAPI)
    │
    ├─→ Validate Input
    ├─→ Store Raw Report in DB
    └─→ Return Report ID
    │
    ▼
Background Worker Picks Up Unprocessed Report
    │
    ├─→ LLM Classification
    │   ├─→ Extract Category
    │   ├─→ Determine Severity
    │   └─→ Summarize Description
    │
    ├─→ Similarity Detection
    │   ├─→ Query Recent Open Issues
    │   ├─→ LLM Similarity Matching
    │   └─→ Decide: New Issue or Link to Existing
    │
    └─→ Update Database
        ├─→ Create/Update Issue
        ├─→ Link Report to Issue
        └─→ Mark Report as Processed
```

### 2. SLA Calculation Flow

```
SLA Worker (Runs every 15 min)
    │
    ▼
Query Recently Resolved Issues
    │
    ▼
For Each Issue:
    ├─→ Calculate Resolution Time
    │   (resolved_at - created_at)
    │
    ├─→ Determine SLA Threshold
    │   (based on category + severity)
    │
    ├─→ Check Compliance
    │   (met_sla = resolution_time <= threshold)
    │
    └─→ Store SLA Metric
```

### 3. Score Computation Flow

```
Score Worker (Runs hourly)
    │
    ▼
For Each Tenant/Area:
    │
    ├─→ Query SLA Metrics (last 30 days)
    ├─→ Calculate Compliance Rate
    ├─→ Calculate Avg Resolution Time
    ├─→ Count Open vs Closed Issues
    │
    ▼
Compute Performance Score
    │
    ├─→ Weight: 70% SLA Compliance
    ├─→ Weight: 30% Resolution Speed
    │
    ▼
Store Performance Score
    │
    └─→ Generate Rankings/Leaderboards
```

## Technology Stack

### Backend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| API Framework | FastAPI | High-performance async HTTP endpoints |
| Language | Python 3.11 | Primary backend language |
| ORM | SQLAlchemy | Database abstraction layer |
| Database | PostgreSQL 15 | Relational data store |
| Connection Pool | psycopg2 | Database connection management |

### Concurrency

| Component | Technology | Use Case |
|-----------|-----------|----------|
| I/O-Bound Tasks | ThreadPoolExecutor | Database queries, API calls, LLM requests |
| CPU-Bound Tasks | ProcessPoolExecutor | Heavy analytics, data aggregation |
| Scheduling | Custom Scheduler | Periodic background job execution |

### LLM Integration

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Client | OpenAI-compatible API | Generic LLM wrapper |
| Classification | GPT-4 | Category and severity detection |
| Similarity | GPT-4 | Report deduplication |
| Validation | JSON Schema | LLM response validation |

### Infrastructure

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Compute | AWS EC2 | Application hosting |
| Database | AWS RDS (PostgreSQL) | Managed database |
| Containers | Docker + Docker Compose | Local & deployment packaging |
| Future Queue | Redis / AWS SQS | Message queue for scaling |

## Database Schema

### Core Tables

#### `tenants`
Primary entities (cities, buildings, campuses, etc.)
- `id` (PK)
- `name`
- `type` (city, building, campus, hotel, facility)
- `created_at`

#### `areas`
Sub-zones within a tenant
- `id` (PK)
- `tenant_id` (FK → tenants)
- `name`
- `created_at`

#### `issues`
Grouped incident issues
- `id` (PK)
- `tenant_id` (FK → tenants)
- `area_id` (FK → areas)
- `category` (infrastructure, sanitation, safety, etc.)
- `severity` (low, medium, high, critical)
- `status` (open, in-progress, resolved, closed)
- `created_at`
- `resolved_at`

#### `reports`
Individual report submissions
- `id` (PK)
- `issue_id` (FK → issues)
- `tenant_id` (FK → tenants)
- `description` (text)
- `location`
- `submitted_at`
- `processed` (boolean)

#### `sla_metrics`
SLA performance tracking
- `id` (PK)
- `issue_id` (FK → issues)
- `resolution_time_hours`
- `met_sla` (boolean)
- `calculated_at`

#### `performance_scores`
Aggregated performance metrics
- `id` (PK)
- `tenant_id` (FK → tenants)
- `area_id` (FK → areas)
- `score` (decimal)
- `metric_type`
- `calculated_at`

### Key Indexes

```sql
-- High-traffic query optimization
CREATE INDEX idx_reports_tenant ON reports(tenant_id);
CREATE INDEX idx_reports_issue ON reports(issue_id);
CREATE INDEX idx_issues_tenant ON issues(tenant_id);
CREATE INDEX idx_issues_status ON issues(status);
CREATE INDEX idx_sla_issue ON sla_metrics(issue_id);
```

## Concurrency Patterns

### Producer-Consumer Pattern

```python
# Ingestion → Processing → Storage

# Producer: API receives reports
@app.post("/reports/")
async def submit_report(data):
    report = store_report(data)  # Fast write
    return {"id": report.id}

# Consumer: Background worker processes
def process_reports():
    with ThreadPoolExecutor(max_workers=10) as executor:
        reports = fetch_unprocessed_reports()
        futures = [executor.submit(classify_and_link, r) for r in reports]
        for future in as_completed(futures):
            result = future.result()
```

### I/O vs CPU Task Separation

```python
# I/O-bound: Use threads
def classify_with_llm(report):
    # Network call to LLM API
    return llm_client.classify(report.description)

# CPU-bound: Use processes
def compute_complex_analytics(tenant_data):
    # Heavy computation
    return aggregate_metrics(tenant_data)

# Worker orchestration
thread_pool = ThreadPoolExecutor(max_workers=20)
process_pool = ProcessPoolExecutor(max_workers=4)

thread_pool.submit(classify_with_llm, report)
process_pool.submit(compute_complex_analytics, data)
```

## Multi-Tenancy Model

### Tenant Isolation

- **Data Level**: All tables include `tenant_id` for row-level isolation
- **Query Level**: All queries filter by `tenant_id`
- **API Level**: Tenant context derived from authentication/session

### Configurable Rules

Each tenant can have custom:
- SLA thresholds per category/severity
- Issue categories
- Scoring weights
- Dashboard preferences

## Scaling Considerations

### Horizontal Scaling

1. **Stateless API Servers**: Multiple FastAPI instances behind load balancer
2. **Worker Scaling**: Independent worker processes for each job type
3. **Database Read Replicas**: Separate read/write paths

### Performance Optimization

1. **Connection Pooling**: Reuse database connections
2. **Batch Processing**: Process reports in batches vs one-at-a-time
3. **Caching**: Cache frequently accessed tenant configs
4. **Async I/O**: FastAPI's async capabilities for concurrent requests

## Security Considerations

1. **Database**: 
   - RDS in private subnet
   - Security groups restricting access
   - Encrypted at rest and in transit

2. **API**:
   - Authentication tokens (future)
   - Rate limiting (future)
   - Input validation

3. **LLM Integration**:
   - API keys in environment variables
   - Request/response logging for audit

## Future Enhancements

### Phase 2
- Message queue (Redis/SQS) for better job distribution
- Real-time websocket updates for dashboards
- Advanced NLP for report analysis

### Phase 3
- Kubernetes deployment for auto-scaling
- GraphQL API for flexible queries
- Machine learning models for prediction

### Phase 4
- Mobile app for report submission
- Public API for third-party integrations
- Advanced analytics and reporting engine
