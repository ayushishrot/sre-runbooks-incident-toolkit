# Error-Budget Policy

The error budget is the amount of unreliability an SLO permits over a window. If a
service targets **99.9%** availability over 30 days, the budget is **0.1%** — about
**43 minutes** of allowed unavailability per 30-day window.

This policy turns that number into decisions everyone agrees to in advance, so we are
not negotiating priorities in the middle of an incident.

## Budget thresholds and actions

| Budget remaining (rolling 30d) | What it means | Action |
|--------------------------------|---------------|--------|
| **> 50%** | Healthy | Ship features at normal pace. |
| **10–50%** | Spending faster than ideal | Continue shipping, but every sprint must include at least one reliability item targeting the top burn source. |
| **< 10%** | Nearly exhausted | **Feature freeze.** Only reliability work, bug fixes, and changes approved by the service owner ship. Deploys still allowed but scrutinized. |
| **Exhausted (SLO missed)** | Budget gone before window end | Freeze remains. Mandatory incident/error-budget review. Re-evaluate whether the SLO target is still right. |

"Feature freeze" means new user-facing functionality pauses. It does **not** block
security patches, reliability fixes, or rollback of a bad change.

## Burn-rate alerting (how we detect spend)

We alert on **burn rate** — how fast the budget is being consumed relative to the
window — using multi-window, multi-burn-rate alerts (Google SRE workbook):

| Severity | Burn rate | Long window | Short window | Budget consumed before fire |
|----------|-----------|-------------|--------------|-----------------------------|
| Page (fast) | 14.4x | 1h | 5m | ~2% in 1h |
| Page (medium) | 6x | 6h | 30m | ~5% in 6h |
| Ticket (slow) | 3x | 24h | 2h | ~10% in 24h |

The short window prevents alerting on a burn that has already stopped; both windows
must be over threshold to fire. Rules live in the companion repo
`observability-slo-stack` (`prometheus/rules/slo-burnrate-alerts.yml`).

## Governance

- **Owner:** each service has a named owner accountable for its SLO.
- **Review cadence:** error budgets reviewed weekly in the reliability sync; any
  SEV1/SEV2 triggers an out-of-band review.
- **Exceptions:** a freeze exception requires written sign-off from the service owner
  and is recorded in the incident channel.
- **SLO changes:** targets are revisited quarterly, or after a postmortem shows the
  target is unrealistic or too loose to be meaningful.
