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

for copilot: 
civicpulse-engine/
├── README.md                # Project overview + architecture docs
├── docker-compose.yml       # Local + EC2 MVP deployment
├── .env.example             # Environment variable template
├── Makefile                 # Dev shortcuts (build, run, lint, migrate, etc.)
├── requirements.txt         # Backend Python dependencies
├── pyproject.toml           # Python tooling config (pytest, formatting, etc.)
│
├── sql/
│   └── schema.sql           # PostgreSQL schema (core DB model)
│
├── scripts/
│   ├── seed_dev_data.py     # Populate DB with fake tenants/reports/issues
│   ├── run_migrations.py   # Run schema updates (until Alembic later)
│   ├── simulate_load.py    # Generates fake report traffic (concurrency testing)
│   └── reset_db.py
│
├── app/                     # BACKEND + WORKERS
│   ├── main.py              # FastAPI app startup
│   ├── config.py            # Env-based app config loader
│
│   ├── api/                 # HTTP endpoint definitions
│   │   ├── __init__.py
│   │   ├── routes_reports.py
│   │   ├── routes_issues.py
│   │   ├── routes_scores.py
│   │   └── routes_health.py
│
│   ├── workers/             # BACKGROUND PIPELINES
│   │   ├── __init__.py
│   │   ├── worker_main.py        # Worker entrypoint
│   │   ├── dedup_worker.py       # Issue grouping logic
│   │   ├── sla_worker.py         # SLA timers + calculations
│   │   ├── score_worker.py       # Performance aggregation
│   │   └── scheduler.py          # Batch task coordinator
│
│   ├── llm/                 # LLM INPUT PROCESSING
│   │   ├── __init__.py
│   │   ├── client.py             # Generic OpenAI-style client wrapper
│   │   ├── classify_report.py   # Category + severity detection prompts
│   │   ├── similarity.py        # Matching reports to existing issues
│   │   └── validators.py        # JSON schema validation of LLM results
│
│   ├── domain/              # CORE BUSINESS MODELS
│   │   ├── __init__.py
│   │   ├── issue.py
│   │   ├── report.py
│   │   ├── tenant.py
│   │   ├── area.py
│   │   ├── rating.py
│   │   └── sla.py
│
│   ├── db/                  # DATABASE ACCESS
│   │   ├── __init__.py
│   │   ├── connection.py        # Postgres connection pool
│   │   ├── base.py              # SQLAlchemy Base
│   │   ├── models.py            # ORM models per table
│   │   ├── repositories.py      # CRUD SQL methods
│   │   └── queries.py           # Optimized analytic SQL queries
│
│   ├── analytics/           # METRICS COMPUTATION
│   │   ├── __init__.py
│   │   ├── issue_stats.py       # Issue counts & trends
│   │   ├── performance.py       # SLA metrics
│   │   ├── rankings.py          # Tenant/area leaderboards
│   │   └── time_series.py       # Historical trend builders
│
│   ├── utils/               # SHARED HELPERS
│   │   ├── __init__.py
│   │   ├── geo.py               # Location clustering helpers
│   │   ├── text.py              # Text normalization
│   │   ├── concurrency.py       # Thread/process helpers
│   │   └── logging.py           # App logging config
│
│   └── tests/
│       ├── test_ingestion.py
│       ├── test_dedup.py
│       ├── test_sla.py
│       └── test_llm_parsing.py
│
├── frontend/                # REACT + VITE UI
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── public/
│   │   └── index.html
│
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │
│   │   ├── api/
│   │   │   └── civicpulseApi.ts    # API client wrapper
│   │
│   │   ├── pages/
│   │   │   ├── SubmitIssue.tsx
│   │   │   ├── IssueList.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   └── TenantSelect.tsx
│   │
│   │   ├── components/
│   │   │   ├── IssueCard.tsx
│   │   │   ├── Charts.tsx
│   │   │   ├── Filters.tsx
│   │   │   └── Navbar.tsx
│   │
│   │   ├── types/
│   │   │   └── models.ts
│   │
│   │   └── styles/
│   │       └── theme.css
│
├── infra/                   # DEVOPS & DEPLOYMENT
│   ├── docker/
│   │   ├── Dockerfile.api
│   │   ├── Dockerfile.worker
│   │   └── Dockerfile.frontend
│
│   ├── aws/
│   │   └── ecs-task-def.json     # Later scaling support
│
│   └── k8s/                      # Optional future work
│       ├── api-deployment.yaml
│       ├── worker-deployment.yaml
│       └── service.yaml
│
└── docs/
    ├── ARCHITECTURE.md
    ├── API_SPEC.md
    └── PERFORMANCE_NOTES.md
