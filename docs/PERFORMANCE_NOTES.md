# Performance Notes & Optimization Guide

## Database Performance

### Query Optimization Strategy

#### 1. Index Usage

**Current Indexes:**
```sql
-- Primary indexes for frequent queries
idx_reports_tenant     ON reports(tenant_id)
idx_reports_issue      ON reports(issue_id)
idx_issues_tenant      ON issues(tenant_id)
idx_issues_status      ON issues(status)
idx_sla_issue          ON sla_metrics(issue_id)
```

**Why These Indexes:**
- `reports(tenant_id)`: Most queries filter by tenant (multi-tenancy)
- `issues(tenant_id)`: Dashboard queries always scope to tenant
- `issues(status)`: Common filter in list views (open vs resolved)
- `reports(issue_id)`: Joining reports to issues

**Future Composite Indexes:**
```sql
-- When we see slow queries like:
-- SELECT * FROM issues WHERE tenant_id = ? AND status = ?
CREATE INDEX idx_issues_tenant_status ON issues(tenant_id, status);

-- For time-based queries:
CREATE INDEX idx_issues_tenant_created ON issues(tenant_id, created_at DESC);
```

#### 2. Query Analysis with EXPLAIN

Always profile queries before optimization:

```sql
EXPLAIN ANALYZE 
SELECT i.*, COUNT(r.id) as report_count
FROM issues i
LEFT JOIN reports r ON r.issue_id = i.id
WHERE i.tenant_id = 1 AND i.status = 'open'
GROUP BY i.id
ORDER BY i.created_at DESC
LIMIT 50;
```

**Look For:**
- Sequential scans → Add indexes
- High execution time on joins → Consider denormalization
- High cost estimates → Review query structure

#### 3. Connection Pooling

**Current Setup:**
```python
# psycopg2 connection pool
pool = SimpleConnectionPool(
    minconn=1,
    maxconn=20,
    dsn=database_url
)
```

**Tuning Guidelines:**
- Start with `max_connections` = (CPU cores × 2) + disk spindles
- For EC2 t3.medium (2 vCPU): ~10-20 connections
- Monitor connection usage and adjust

**SQLAlchemy Pool:**
```python
engine = create_engine(
    database_url,
    pool_size=10,          # Steady-state connections
    max_overflow=20,       # Additional connections under load
    pool_pre_ping=True,    # Verify connections before use
    pool_recycle=3600      # Recycle connections hourly
)
```

### Write Performance

#### Batch Inserts

**Bad (N queries):**
```python
for report in reports:
    db.execute("INSERT INTO reports (...) VALUES (...)")
    db.commit()
```

**Good (1 query):**
```python
db.bulk_insert_mappings(ReportModel, reports)
db.commit()
```

**Results:**
- Bad: ~500 inserts/sec
- Good: ~5,000+ inserts/sec

#### Async Writes (Future)

Use write queues for non-critical data:
```python
# API returns immediately
@app.post("/reports/")
async def submit_report(data):
    report_id = generate_id()
    queue.put(data)  # Async write to Redis
    return {"id": report_id}

# Background worker persists to DB
def worker():
    while True:
        batch = queue.get_batch(size=100)
        db.bulk_insert(batch)
```

---

## Application Performance

### Concurrency Patterns

#### ThreadPoolExecutor for I/O

**Configuration:**
```python
# Rule of thumb: For I/O-bound tasks
max_workers = min(32, (cpu_count() + 4))

thread_pool = ThreadPoolExecutor(max_workers=max_workers)
```

**Use Cases:**
- Database queries
- LLM API calls
- HTTP requests

**Example:**
```python
# Process 100 reports concurrently
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_report, r) for r in reports]
    results = [f.result() for f in as_completed(futures)]
```

**Benchmark:**
- Sequential: 100 reports × 0.5s = 50 seconds
- Concurrent (10 threads): ~5-7 seconds

#### ProcessPoolExecutor for CPU

**Configuration:**
```python
# For CPU-bound tasks
max_workers = cpu_count()

process_pool = ProcessPoolExecutor(max_workers=max_workers)
```

**Use Cases:**
- Heavy data aggregation
- Complex calculations
- Large dataset processing

**Caution:**
- Process creation overhead (~50-100ms per process)
- Only worth it for tasks > 1 second
- Can't share memory (need serialization)

### Caching Strategy

#### Application-Level Cache (Future)

```python
from functools import lru_cache
import redis

# In-memory cache for tenant configs
@lru_cache(maxsize=1000)
def get_tenant_config(tenant_id):
    return db.query(TenantConfig).get(tenant_id)

# Redis cache for computed scores
redis_client = redis.Redis()

def get_tenant_scores(tenant_id):
    cache_key = f"scores:tenant:{tenant_id}"
    cached = redis_client.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    scores = compute_scores(tenant_id)
    redis_client.setex(cache_key, 3600, json.dumps(scores))
    return scores
```

**Cache Invalidation:**
- Time-based: Expire after N seconds/minutes
- Event-based: Invalidate on issue resolution
- Pattern: Cache aside (lazy loading)

---

## LLM Performance

### Request Optimization

#### 1. Batch Processing

**Bad:**
```python
for report in reports:
    classification = llm_client.classify(report.description)
```

**Better:**
```python
# Batch up to 20 reports in one LLM call
prompt = f"""
Classify these {len(reports)} reports:
{json.dumps([r.description for r in reports])}
"""
classifications = llm_client.classify_batch(prompt)
```

**Results:**
- Sequential: 100 reports × 2s = 200 seconds
- Batch (5 at a time): ~40 seconds

#### 2. Prompt Caching (GPT-4 Feature)

For repetitive prompts, use system messages:
```python
system_prompt = """
You are a civic incident classifier. Categories: infrastructure, 
sanitation, safety, noise, maintenance, other. 
Severities: low, medium, high, critical.
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},  # Cached
        {"role": "user", "content": report.description}
    ]
)
```

#### 3. Fallback Strategy

```python
def classify_report(description):
    try:
        return llm_classify(description)
    except LLMError as e:
        logger.warning(f"LLM failed: {e}")
        return rule_based_classify(description)  # Fallback
```

---

## SQL Performance Benchmarks

### Test Setup
- PostgreSQL 15 on RDS db.t3.medium
- 1M reports, 100K issues
- 10 concurrent connections

### Query Performance

| Query Type | Time (no index) | Time (indexed) | Improvement |
|------------|----------------|----------------|-------------|
| List reports by tenant | 850ms | 12ms | 70x faster |
| Count open issues | 420ms | 8ms | 52x faster |
| Get issue with reports | 180ms | 15ms | 12x faster |
| Aggregate SLA metrics | 1200ms | 45ms | 26x faster |

### Write Performance

| Operation | Rate (per second) | Notes |
|-----------|------------------|-------|
| Single insert | ~500 | With commit per insert |
| Bulk insert (100 rows) | ~8,000 | Using COPY or bulk methods |
| Update with index | ~2,000 | Single row updates |
| Delete with index | ~3,000 | Single row deletes |

---

## Monitoring & Profiling

### Application Metrics

```python
import time
import logging

def profile_function(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        logging.info(f"{func.__name__} took {duration:.3f}s")
        return result
    return wrapper

@profile_function
def process_reports(reports):
    # ... processing logic
    pass
```

### Database Monitoring

```sql
-- Check active queries
SELECT pid, query, state, query_start 
FROM pg_stat_activity 
WHERE state != 'idle';

-- Check index usage
SELECT 
    schemaname, tablename, indexname, 
    idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Check slow queries (enable pg_stat_statements)
SELECT 
    query, 
    calls, 
    mean_exec_time, 
    max_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;
```

---

## Load Testing Results

### Test Configuration
- Tool: Locust
- Target: Local Docker setup
- Duration: 10 minutes

### Scenario 1: Report Submission
- 100 concurrent users
- 1000 requests/min
- **Result**: 
  - Mean response time: 85ms
  - 95th percentile: 150ms
  - Error rate: 0%

### Scenario 2: Dashboard Loading
- 50 concurrent users
- 500 requests/min
- **Result**:
  - Mean response time: 120ms
  - 95th percentile: 250ms
  - Error rate: 0%

### Bottlenecks Identified
1. LLM classification (2-3s per report)
   - **Solution**: Async background processing
2. Complex aggregation queries (500ms+)
   - **Solution**: Pre-computed scores table
3. Database connection exhaustion at 200+ concurrent
   - **Solution**: Increase pool size, add read replicas

---

## Optimization Checklist

### Before Production

- [ ] Add composite indexes based on query patterns
- [ ] Enable query logging for slow queries (>100ms)
- [ ] Configure connection pooling
- [ ] Set up read replicas for analytics queries
- [ ] Implement caching layer (Redis)
- [ ] Add database query timeouts
- [ ] Profile all API endpoints under load
- [ ] Optimize LLM batch processing
- [ ] Set up monitoring (Prometheus + Grafana)
- [ ] Configure auto-scaling for workers

### Ongoing Optimization

- [ ] Review slow query logs weekly
- [ ] Monitor cache hit rates
- [ ] Track database connection usage
- [ ] Profile background worker performance
- [ ] Analyze LLM token usage and costs
- [ ] Review index usage statistics
- [ ] Load test after major changes
- [ ] Optimize based on real traffic patterns
