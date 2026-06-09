# SLO Catalog

Example SLOs by service tier. Each SLO names an SLI (the measurement), a target, and a
window. Targets are deliberately *achievable*  an SLO you always meet by a wide margin
is set too low to be useful; one you always miss erodes trust in the number.

## Tiers

| Tier | Description | Default availability SLO | Latency SLO |
|------|-------------|--------------------------|-------------|
| **0  critical** | Revenue path, auth | 99.95% / 30d | p99 < 300ms |
| **1  core** | Primary product APIs | 99.9% / 30d | p99 < 500ms |
| **2  supporting** | Internal/back-office | 99.5% / 30d | p99 < 1s |

## SLI definitions

**Availability (request-based):**

```
sli = sum(rate(http_requests_total{job="$svc",code!~"5.."}[window]))
      / sum(rate(http_requests_total{job="$svc"}[window]))
```

**Latency (good-events ratio):**

```
sli = sum(rate(http_request_duration_seconds_bucket{job="$svc",le="0.5"}[window]))
      / sum(rate(http_request_duration_seconds_count{job="$svc"}[window]))
```

## Example service SLOs

| Service | Tier | SLI | Target | Window |
|---------|------|-----|--------|--------|
| `orders` | 0 | success ratio (non-5xx) | 99.95% | 30d rolling |
| `orders` | 0 | p99 latency < 300ms | 99% of requests | 30d rolling |
| `payments` | 0 | success ratio | 99.95% | 30d rolling |
| `catalog` | 1 | success ratio | 99.9% | 30d rolling |
| `kafka-consumers` | 1 | consumer lag < 10k msgs | 99% of 1m samples | 7d rolling |

Recording rules and burn-rate alerts implementing these live in the
`observability-slo-stack` repo.
