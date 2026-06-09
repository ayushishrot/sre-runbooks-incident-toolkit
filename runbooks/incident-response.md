# Incident Response Runbook

How we run an incident from page to resolution. The goal is fast, calm coordination 
clear roles, predictable comms, and a bias toward mitigation over diagnosis.

## Roles

| Role | Who | Responsibility |
|------|-----|----------------|
| **Incident Commander (IC)** | First responder, until handed off | Owns the incident. Coordinates, decides, delegates. Does *not* debug hands-on. |
| **Ops/Tech Lead** | SME for the affected system | Drives investigation and mitigation. |
| **Comms** | IC may delegate | Updates status page + stakeholders on cadence. |
| **Scribe** | Optional, SEV1/2 | Timestamps actions in the incident channel for the postmortem. |

For small incidents one person may hold multiple roles. For SEV1, split IC and Ops.

## Flow

1. **Acknowledge** the page within the on-call SLA (5 min). Run `scripts/ack-page.sh`.
2. **Declare** in `#incidents`: open a channel/thread, state suspected severity, assume IC.
3. **Assess** against the [severity matrix](severity-matrix.md). Set severity explicitly.
4. **Stabilize first.** Prefer reversible mitigation  roll back the last deploy, fail
   over, shed load, scale out  *before* root-causing. A known-good rollback beats a
   clever fix under pressure.
5. **Communicate** on cadence (see below). Post the first update within 15 minutes.
6. **Resolve** once the SLI recovers and is stable. Announce resolution.
7. **Follow up.** Schedule a blameless postmortem within 48h for SEV1/SEV2.

## Communication cadence

| Severity | Internal update | External/status page |
|----------|-----------------|----------------------|
| SEV1 | Every 30 min | Every 30–60 min |
| SEV2 | Every 60 min | As warranted |
| SEV3/4 | At resolution | Usually none |

Updates state: what we know, customer impact, what we are doing, and the next update
time. "No new info, next update in 30 min" is a valid update.

## Common first moves

- **Bad deploy suspected?** Roll back. See service runbooks; for ECS the deployment
  circuit breaker auto-rolls-back, but you can force the previous task def.
- **One AZ/node bad?** Cordon/drain or fail over; let autoscaling replace capacity.
- **Downstream dependency down?** Enable degraded mode / circuit breaker if available;
  communicate reduced functionality rather than total outage.
- **Don't know yet?** Mitigate blast radius (rate limit, feature flag off) and keep
  investigating.

## After resolution

- Capture the timeline while it's fresh (the scribe's notes feed the postmortem).
- File action items with owners.
- If an SLO was breached, the [error-budget policy](../slo/error-budget-policy.md)
  governs what ships next.
