-- PostgreSQL schema (core DB model)

-- Tenants table
CREATE TABLE IF NOT EXISTS tenants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- city, building, campus, hotel, facility
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Areas table (zones within a tenant)
CREATE TABLE IF NOT EXISTS areas (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Issues table (grouped reports)
CREATE TABLE IF NOT EXISTS issues (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    area_id INTEGER REFERENCES areas(id),
    category VARCHAR(100),
    severity VARCHAR(50),
    status VARCHAR(50) DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

-- Reports table (individual submissions)
CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    issue_id INTEGER REFERENCES issues(id),
    tenant_id INTEGER REFERENCES tenants(id),
    description TEXT NOT NULL,
    location VARCHAR(255),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);

-- SLA metrics table
CREATE TABLE IF NOT EXISTS sla_metrics (
    id SERIAL PRIMARY KEY,
    issue_id INTEGER REFERENCES issues(id),
    resolution_time_hours DECIMAL,
    met_sla BOOLEAN,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance scores table
CREATE TABLE IF NOT EXISTS performance_scores (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    area_id INTEGER REFERENCES areas(id),
    score DECIMAL NOT NULL,
    metric_type VARCHAR(100),
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_reports_tenant ON reports(tenant_id);
CREATE INDEX IF NOT EXISTS idx_reports_issue ON reports(issue_id);
CREATE INDEX IF NOT EXISTS idx_issues_tenant ON issues(tenant_id);
CREATE INDEX IF NOT EXISTS idx_issues_status ON issues(status);
CREATE INDEX IF NOT EXISTS idx_sla_issue ON sla_metrics(issue_id);
