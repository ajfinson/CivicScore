export interface Tenant {
  id: number
  name: string
  type: 'city' | 'building' | 'campus' | 'hotel' | 'facility'
  created_at: string
}

export interface Area {
  id: number
  tenant_id: number
  name: string
  created_at: string
}

export interface Issue {
  id: number
  tenant_id: number
  area_id?: number
  category: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  status: 'open' | 'in-progress' | 'resolved' | 'closed'
  created_at: string
  resolved_at?: string
}

export interface Report {
  id: number
  issue_id?: number
  tenant_id: number
  description: string
  location?: string
  submitted_at: string
  processed: boolean
}

export interface SLAMetric {
  id: number
  issue_id: number
  resolution_time_hours: number
  met_sla: boolean
  calculated_at: string
}

export interface PerformanceScore {
  id: number
  tenant_id: number
  area_id?: number
  score: number
  metric_type: string
  calculated_at: string
}
