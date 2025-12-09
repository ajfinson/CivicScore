A multi-tenant incident ingestion, classification & analytics platform for cities, buildings, campuses, hotels, and public facilities.

CivicPulse Engine collects citizen or customer issue reports, groups and prioritizes them, tracks resolution workflows, computes SLA metrics, and generates public or private accountability dashboards — all from a single configurable core engine.

The project is built primarily as a systems engineering & backend learning platform focused on:

- High-volume ingestion pipelines

- SQL modeling & indexing optimization

- Python concurrency (threads + processes)

- Distributed background analytics

- Cloud deployment on AWS

flowchart TB

%% ===============================
%% ACTORS
%% ===============================
Users([Residents / Tenants / Staff])

%% ===============================
%% API LAYER
%% ===============================
API[API Gateway<br/>FastAPI<br/>Auth + Validation]

%% ===============================
%% INGESTION
%% ===============================
Ingest[Ingestion Service<br/>Input Normalization]

LLM[LLM Classification Layer<br/>- Category extraction<br/>- Severity detection<br/>- Issue similarity matching]

%% ===============================
%% WORKER ENGINE
%% ===============================
Workers[Background Analytics Engine<br/>ThreadPool + ProcessPool]

Core[Core Analytics Engine<br/>- Issue deduplication<br/>- Status workflows<br/>- SLA computation<br/>- Priority scoring<br/>- Ranking aggregation]

%% ===============================
%% STORAGE
%% ===============================
DB[(PostgreSQL on AWS RDS<br/>Multi-Tenant Relational Store)]

%% ===============================
%% OUTPUT
%% ===============================
Dashboards[Dashboards & Public/Private Views<br/>Tenant-configured KPIs]

%% ===============================
%% FLOW
%% ===============================
Users --> API --> Ingest --> LLM --> DB

DB <--> Workers --> Core --> DB

DB --> Dashboards
