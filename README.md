A multi-tenant incident ingestion, classification & analytics platform for cities, buildings, campuses, hotels, and public facilities.

CivicPulse Engine collects citizen or customer issue reports, groups and prioritizes them, tracks resolution workflows, computes SLA metrics, and generates public or private accountability dashboards — all from a single configurable core engine.

The project is built primarily as a systems engineering & backend learning platform focused on:

- High-volume ingestion pipelines

- SQL modeling & indexing optimization

- Python concurrency (threads + processes)

- Distributed background analytics

- Cloud deployment on AWS

                       Users
             (Residents, Tenants, Staff)
                          │
                          ▼
                   API Gateway
                     (FastAPI)
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
 Ingestion Service   Query API        Dashboard API
 (Report submits)
        │
        ▼
 Background Processing & Scoring Engine
(ThreadPool + ProcessPool)
        │
        ▼
────────────── CORE ANALYTICS ENGINE ──────────────
- Issue grouping / deduplication
- SLA computations
- Trend metrics & rankings
- Multi-tenant rule evaluation
───────────────────────────────────────────────────
                          │
                          ▼
                  PostgreSQL (AWS RDS)
         Multi-tenant relational data store
                          │
                          ▼
                    Score Dashboards
               (per-tenant, configurable)

                          ▲
                          │
                    LLM Classification
         (Resume/complaint/JD style NLP parsing)
             - Category inference
             - Severity extraction
             - Similarity detection
| Layer                | Technology                               |
| -------------------- | ---------------------------------------- |
| API                  | **FastAPI**                              |
| Workers              | **Python 3.11**                          |
| Concurrency          | ThreadPoolExecutor + ProcessPoolExecutor |
| NLP / Classification | LLM (OpenAI-compatible API)              |
| Database             | PostgreSQL 15 (AWS RDS)                  |
| ORM                  | SQLAlchemy (future)                      |
| Infrastructure       | AWS EC2 + Docker Compose                 |
| Queueing (future)    | Redis / AWS SQS                          |
| Metrics              | Custom aggregation engine                |
| Dashboards           | REST/JSON frontend (future React UI)     |

This project is primarily designed to explore:

✅ SQL Performance Engineering

Query planning (EXPLAIN ANALYZE)

Composite vs partial indexing

Read/write tradeoffs under concurrency

✅ Python Concurrency Patterns

Queue-based pipelines

Separation of IO-bound vs CPU-bound workloads

Producer → Worker → Aggregator patterns

✅ Distributed Systems Fundamentals

Stateless process scaling

Background job orchestration

Snapshot-based reporting

✅ Cloud Engineering

EC2 provisioning

Secure RDS networking

Docker deployment patterns

Environment variable configuration
