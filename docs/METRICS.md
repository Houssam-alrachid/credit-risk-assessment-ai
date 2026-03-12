# Prometheus Metrics Documentation

## Overview

The Credit Risk Assessment AI system exposes Prometheus metrics for comprehensive monitoring and observability. Metrics are collected automatically during workflow execution and exposed via the `/metrics` endpoint.

## Metrics Endpoint

**URL:** `GET /metrics`  
**Format:** Prometheus text format  
**Authentication:** None (configure firewall/network policies for production)

## Available Metrics

### Workflow-Level Metrics

#### `workflow_duration_seconds`
- **Type:** Histogram
- **Description:** Total duration of credit assessment workflow execution
- **Labels:** None
- **Buckets:** 5, 10, 15, 20, 25, 30, 40, 50, 60 seconds

```promql
# Average workflow duration over 5 minutes
rate(workflow_duration_seconds_sum[5m]) / rate(workflow_duration_seconds_count[5m])

# 95th percentile workflow duration
histogram_quantile(0.95, rate(workflow_duration_seconds_bucket[5m]))
```

#### `workflow_total`
- **Type:** Counter
- **Description:** Total number of workflow executions
- **Labels:** 
  - `status`: success, error

```promql
# Workflow success rate
rate(workflow_total{status="success"}[5m]) / rate(workflow_total[5m])

# Total workflows processed
sum(workflow_total)
```

#### `workflow_active`
- **Type:** Gauge
- **Description:** Number of currently active/running workflows
- **Labels:** None

```promql
# Current active workflows
workflow_active

# Peak concurrent workflows in last hour
max_over_time(workflow_active[1h])
```

### Node-Level Metrics

#### `node_duration_seconds`
- **Type:** Histogram
- **Description:** Execution duration of individual workflow nodes
- **Labels:**
  - `node_name`: collect_financial_data, analyze_income, analyze_debt, evaluate_collateral, sync_parallel_analyses, calculate_risk, write_decision
- **Buckets:** 1, 2, 3, 4, 5, 7, 10, 15, 20 seconds

```promql
# Average duration per node
rate(node_duration_seconds_sum[5m]) / rate(node_duration_seconds_count[5m]) by (node_name)

# Slowest nodes (95th percentile)
histogram_quantile(0.95, rate(node_duration_seconds_bucket[5m])) by (node_name)
```

#### `node_total`
- **Type:** Counter
- **Description:** Total number of node executions
- **Labels:**
  - `node_name`: Node identifier
  - `status`: success, error

```promql
# Node error rate
rate(node_total{status="error"}[5m]) / rate(node_total[5m]) by (node_name)

# Most frequently executed nodes
sum(rate(node_total[5m])) by (node_name)
```

### LLM Metrics

#### `llm_tokens_total`
- **Type:** Counter
- **Description:** Total LLM tokens consumed
- **Labels:**
  - `direction`: input, output
  - `agent`: financial_data_collector, income_analyzer, debt_analyzer, collateral_evaluator, risk_scorer, decision_writer

```promql
# Total tokens per minute
rate(llm_tokens_total[1m])

# Token usage by agent
sum(rate(llm_tokens_total[5m])) by (agent, direction)

# Cost estimation (assuming $0.15 per 1M input tokens, $0.60 per 1M output tokens)
(rate(llm_tokens_total{direction="input"}[5m]) * 0.15 / 1000000) + 
(rate(llm_tokens_total{direction="output"}[5m]) * 0.60 / 1000000)
```

#### `llm_calls_total`
- **Type:** Counter
- **Description:** Total number of LLM API calls
- **Labels:**
  - `agent`: Agent name
  - `status`: success, error

```promql
# LLM call success rate
rate(llm_calls_total{status="success"}[5m]) / rate(llm_calls_total[5m]) by (agent)

# Failed LLM calls
sum(rate(llm_calls_total{status="error"}[5m])) by (agent)
```

#### `llm_latency_seconds`
- **Type:** Histogram
- **Description:** LLM API call latency
- **Labels:**
  - `agent`: Agent name
- **Buckets:** 0.5, 1, 2, 3, 4, 5, 7, 10 seconds

```promql
# Average LLM latency by agent
rate(llm_latency_seconds_sum[5m]) / rate(llm_latency_seconds_count[5m]) by (agent)

# 99th percentile LLM latency
histogram_quantile(0.99, rate(llm_latency_seconds_bucket[5m])) by (agent)
```

### Error Metrics

#### `errors_total`
- **Type:** Counter
- **Description:** Total number of errors
- **Labels:**
  - `error_type`: Exception class name (e.g., ValueError, HTTPError)
  - `component`: Component where error occurred (workflow, node name)

```promql
# Error rate by type
sum(rate(errors_total[5m])) by (error_type)

# Errors by component
sum(rate(errors_total[5m])) by (component)

# Most common errors
topk(5, sum(rate(errors_total[5m])) by (error_type))
```

## Example Queries

### Performance Monitoring

```promql
# Average end-to-end processing time
avg(rate(workflow_duration_seconds_sum[5m]) / rate(workflow_duration_seconds_count[5m]))

# Parallel execution efficiency (compare parallel nodes vs sequential)
avg(rate(node_duration_seconds_sum{node_name=~"analyze_income|analyze_debt|evaluate_collateral"}[5m]) / 
    rate(node_duration_seconds_count{node_name=~"analyze_income|analyze_debt|evaluate_collateral"}[5m]))
```

### Reliability Monitoring

```promql
# Overall success rate
sum(rate(workflow_total{status="success"}[5m])) / sum(rate(workflow_total[5m]))

# Error rate trend
sum(rate(errors_total[5m]))
```

### Cost Monitoring

```promql
# Estimated hourly cost (GPT-4o-mini pricing)
(sum(rate(llm_tokens_total{direction="input"}[1h])) * 0.15 / 1000000 + 
 sum(rate(llm_tokens_total{direction="output"}[1h])) * 0.60 / 1000000) * 3600
```

### Capacity Planning

```promql
# Peak concurrent workflows
max_over_time(workflow_active[24h])

# Throughput (assessments per hour)
sum(rate(workflow_total[1h])) * 3600
```

## Grafana Dashboard

### Recommended Panels

1. **Workflow Duration** (Graph)
   - Query: `histogram_quantile(0.95, rate(workflow_duration_seconds_bucket[5m]))`
   - Shows 95th percentile processing time

2. **Throughput** (Graph)
   - Query: `sum(rate(workflow_total[5m])) * 60`
   - Shows assessments per minute

3. **Success Rate** (Gauge)
   - Query: `sum(rate(workflow_total{status="success"}[5m])) / sum(rate(workflow_total[5m])) * 100`
   - Shows percentage

4. **Active Workflows** (Graph)
   - Query: `workflow_active`
   - Shows current concurrency

5. **Node Performance** (Heatmap)
   - Query: `sum(rate(node_duration_seconds_bucket[5m])) by (node_name, le)`
   - Shows duration distribution per node

6. **Token Usage** (Graph)
   - Query: `sum(rate(llm_tokens_total[5m])) by (direction)`
   - Shows input/output token rate

7. **Error Rate** (Graph)
   - Query: `sum(rate(errors_total[5m])) by (error_type)`
   - Shows errors by type

## Alerting Rules

### Critical Alerts

```yaml
groups:
  - name: credit_assessment_critical
    rules:
      - alert: HighErrorRate
        expr: sum(rate(workflow_total{status="error"}[5m])) / sum(rate(workflow_total[5m])) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High workflow error rate ({{ $value | humanizePercentage }})"
          
      - alert: SlowWorkflowExecution
        expr: histogram_quantile(0.95, rate(workflow_duration_seconds_bucket[5m])) > 30
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "95th percentile workflow duration exceeds 30s"
          
      - alert: LLMAPIFailures
        expr: sum(rate(llm_calls_total{status="error"}[5m])) > 0.5
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "LLM API experiencing failures"
```

## Integration

### Prometheus Configuration

```yaml
scrape_configs:
  - job_name: 'credit-assessment-api'
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### Docker Compose

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

## Best Practices

1. **Scrape Interval:** Use 15-30 second intervals for production
2. **Retention:** Keep metrics for at least 30 days
3. **Cardinality:** Monitor label cardinality to avoid explosion
4. **Dashboards:** Create role-specific dashboards (ops, business, dev)
5. **Alerts:** Set up alerts for SLOs (e.g., 95% success rate, <20s p95 latency)

## Troubleshooting

### High Latency
```promql
# Identify slow nodes
topk(3, avg(rate(node_duration_seconds_sum[5m]) / rate(node_duration_seconds_count[5m])) by (node_name))
```

### Memory Issues
```promql
# Check for workflow buildup
workflow_active > 50
```

### Cost Spikes
```promql
# Identify high token consumers
topk(3, sum(rate(llm_tokens_total[1h])) by (agent))
```
