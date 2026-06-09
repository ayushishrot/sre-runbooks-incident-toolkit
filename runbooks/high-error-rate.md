# Runbook: High Error Rate (5xx burn)

**Trigger:** SLO burn-rate alert `HighErrorRateFastBurn` / page from `#alerts`.

## 1. Confirm impact
- Grafana → service SLO dashboard. Is the success-ratio SLI actually dropping, or is it
  a single noisy instance?
- Check `sum by (code) (rate(http_requests_total{job="$svc"}[5m]))` for the dominant
  error code.

## 2. Correlate with change
- Did we deploy in the last 30 min? `kubectl rollout history` / ECS deployment events.
- **If yes → roll back first.** Rollback beats root-causing under an active burn.

## 3. Common causes & moves
| Symptom | Likely cause | Move |
|---------|--------------|------|
| 5xx right after deploy | Bad release | Roll back to previous version |
| 5xx + DB connection errors | Pool exhausted / DB down | Scale DB connections, check RDS; failover if needed |
| 503 from LB | No healthy targets | Check task/pod health, readiness probe, scale out |
| 5xx on one AZ | Zonal fault | Drain/cordon affected nodes, let ASG replace |

## 4. Stabilize
Roll back, scale out, or shed load (rate limit / feature flag) until the SLI recovers.

## 5. Resolve & follow up
Announce resolution once the burn-rate alert clears and stays clear for 10 min. File a
postmortem if SEV1/SEV2.
