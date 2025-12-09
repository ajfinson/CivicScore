# CivicPulse Engine API Specification

Base URL: `http://localhost:8000` (development)

## Authentication

Currently no authentication required (development only).
Future: Bearer token authentication.

---

## Health & Status Endpoints

### GET /health

Health check endpoint.

**Response 200:**
```json
{
  "status": "healthy"
}
```

### GET /ready

Readiness check (validates dependencies).

**Response 200:**
```json
{
  "status": "ready"
}
```

---

## Reports Endpoints

### POST /reports/

Submit a new incident report.

**Request Body:**
```json
{
  "tenant_id": 1,
  "description": "Pothole on Main Street near the intersection",
  "location": "Main St & 1st Ave"
}
```

**Response 201:**
```json
{
  "message": "Report submitted",
  "id": 42
}
```

**Validation:**
- `tenant_id`: required, integer > 0
- `description`: required, string, min 10 chars
- `location`: optional, string

---

### GET /reports/{report_id}

Get a specific report by ID.

**Path Parameters:**
- `report_id`: integer

**Response 200:**
```json
{
  "id": 42,
  "tenant_id": 1,
  "issue_id": 15,
  "description": "Pothole on Main Street near the intersection",
  "location": "Main St & 1st Ave",
  "submitted_at": "2025-12-09T10:30:00Z",
  "processed": true
}
```

**Response 404:**
```json
{
  "detail": "Report not found"
}
```

---

### GET /reports/

List all reports with optional filtering.

**Query Parameters:**
- `tenant_id`: integer (optional) - Filter by tenant
- `skip`: integer, default 0 - Pagination offset
- `limit`: integer, default 100, max 1000 - Results per page

**Response 200:**
```json
{
  "reports": [
    {
      "id": 42,
      "tenant_id": 1,
      "issue_id": 15,
      "description": "Pothole on Main Street",
      "location": "Main St & 1st Ave",
      "submitted_at": "2025-12-09T10:30:00Z",
      "processed": true
    }
  ],
  "total": 150,
  "skip": 0,
  "limit": 100
}
```

---

## Issues Endpoints

### GET /issues/

List all issues with optional filtering.

**Query Parameters:**
- `tenant_id`: integer (optional) - Filter by tenant
- `status`: string (optional) - Filter by status (open, in-progress, resolved, closed)

**Response 200:**
```json
{
  "issues": [
    {
      "id": 15,
      "tenant_id": 1,
      "area_id": 3,
      "category": "infrastructure",
      "severity": "high",
      "status": "open",
      "created_at": "2025-12-08T14:20:00Z",
      "resolved_at": null,
      "report_count": 5
    }
  ]
}
```

---

### GET /issues/{issue_id}

Get a specific issue by ID.

**Path Parameters:**
- `issue_id`: integer

**Response 200:**
```json
{
  "id": 15,
  "tenant_id": 1,
  "area_id": 3,
  "category": "infrastructure",
  "severity": "high",
  "status": "open",
  "created_at": "2025-12-08T14:20:00Z",
  "resolved_at": null,
  "reports": [
    {
      "id": 42,
      "description": "Pothole on Main Street",
      "location": "Main St & 1st Ave",
      "submitted_at": "2025-12-09T10:30:00Z"
    }
  ]
}
```

---

### PATCH /issues/{issue_id}

Update an issue (e.g., change status).

**Path Parameters:**
- `issue_id`: integer

**Request Body:**
```json
{
  "status": "resolved"
}
```

**Response 200:**
```json
{
  "id": 15,
  "status": "resolved",
  "resolved_at": "2025-12-09T15:45:00Z"
}
```

**Allowed Updates:**
- `status`: open, in-progress, resolved, closed
- `area_id`: integer
- `severity`: low, medium, high, critical

---

## Scores & Dashboard Endpoints

### GET /scores/tenant/{tenant_id}

Get performance scores for a specific tenant.

**Path Parameters:**
- `tenant_id`: integer

**Response 200:**
```json
{
  "tenant_id": 1,
  "scores": {
    "overall": 87.5,
    "sla_compliance": 0.92,
    "average_resolution_hours": 18.5,
    "open_issues": 12,
    "resolved_issues": 145,
    "total_reports": 312
  },
  "period": "last_30_days",
  "calculated_at": "2025-12-09T16:00:00Z"
}
```

---

### GET /scores/area/{area_id}

Get performance scores for a specific area.

**Path Parameters:**
- `area_id`: integer

**Response 200:**
```json
{
  "area_id": 3,
  "tenant_id": 1,
  "scores": {
    "overall": 85.0,
    "sla_compliance": 0.88,
    "average_resolution_hours": 22.3,
    "open_issues": 4,
    "resolved_issues": 38
  },
  "period": "last_30_days",
  "calculated_at": "2025-12-09T16:00:00Z"
}
```

---

### GET /scores/leaderboard

Get rankings across tenants or areas.

**Query Parameters:**
- `tenant_id`: integer (optional) - If provided, rank areas within tenant; otherwise rank all tenants

**Response 200 (Tenant Leaderboard):**
```json
{
  "leaderboard": [
    {
      "rank": 1,
      "tenant_id": 1,
      "name": "City of Springfield",
      "score": 87.5,
      "sla_compliance": 0.92
    },
    {
      "rank": 2,
      "tenant_id": 2,
      "name": "Downtown Tower",
      "score": 82.3,
      "sla_compliance": 0.85
    }
  ],
  "period": "last_30_days",
  "metric": "overall_score"
}
```

---

## Data Models

### Report
```typescript
{
  id: number
  tenant_id: number
  issue_id?: number
  description: string
  location?: string
  submitted_at: string (ISO 8601)
  processed: boolean
}
```

### Issue
```typescript
{
  id: number
  tenant_id: number
  area_id?: number
  category: string  // infrastructure, sanitation, safety, noise, maintenance, other
  severity: string  // low, medium, high, critical
  status: string    // open, in-progress, resolved, closed
  created_at: string (ISO 8601)
  resolved_at?: string (ISO 8601)
}
```

### Performance Score
```typescript
{
  tenant_id: number
  area_id?: number
  scores: {
    overall: number              // 0-100
    sla_compliance: number       // 0-1 (percentage as decimal)
    average_resolution_hours: number
    open_issues: number
    resolved_issues: number
    total_reports?: number
  }
  period: string
  calculated_at: string (ISO 8601)
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limits

Currently no rate limits (development).

Future production limits:
- 100 requests per minute per IP
- 1000 report submissions per hour per tenant

---

## WebSocket Endpoints (Future)

### WS /ws/issues/{tenant_id}

Real-time issue updates for a tenant.

**Message Format:**
```json
{
  "event": "issue_created",
  "data": {
    "id": 15,
    "category": "infrastructure",
    "severity": "high"
  }
}
```

Events:
- `issue_created`
- `issue_updated`
- `issue_resolved`
- `report_submitted`

---

## Pagination

All list endpoints support pagination:
- `skip`: Offset (default 0)
- `limit`: Page size (default 100, max 1000)

Response includes:
```json
{
  "items": [...],
  "total": 500,
  "skip": 0,
  "limit": 100,
  "has_more": true
}
```

---

## Filtering & Sorting (Future)

Query parameters for advanced filtering:
- `created_after`: ISO 8601 date
- `created_before`: ISO 8601 date
- `category`: Filter by category
- `severity`: Filter by severity
- `sort_by`: Field to sort by
- `sort_order`: asc or desc

Example:
```
GET /issues/?tenant_id=1&status=open&severity=high&sort_by=created_at&sort_order=desc
```
