# Postmortem: Payments 5xx spike from connection-pool exhaustion (2026-01-18)

> Blameless. Example postmortem demonstrating the format.

- **Severity:** SEV1
- **Duration:** 14:02 → 14:41 UTC (MTTD: 3m, MTTR: 39m)
- **Author(s):** Ayushi Shrotriya
- **Status:** Reviewed

## Summary
A deploy to `payments` lowered the DB connection-pool size via a bad config default.
Under normal load the pool saturated, requests queued, and the service returned 5xx for
~39 minutes before a rollback restored service. ~2.1% of payment attempts failed during
the window.

## Customer impact
Checkout payment failures for ~39 minutes; estimated 2.1% of attempts in-window. The
Tier-0 `payments` availability SLO (99.95%) consumed ~28% of its 30-day error budget.

## Timeline (UTC)
| Time | Event |
|------|-------|
| 14:00 | Deploy `payments` v3.4.1 |
| 14:02 | `HighErrorRateFastBurn` page; on-call ack |
| 14:08 | IC declared SEV1; DB connection-timeout errors identified |
| 14:22 | Pool-size config change spotted in the release diff |
| 14:35 | Rollback to v3.4.0 initiated |
| 14:41 | Error rate recovered; incident resolved |

## Root cause
A refactor moved `DB_POOL_MAX` to a new config loader whose default (5) silently
overrode the intended value (50). The lower default wasn't caught because staging runs
at low concurrency where 5 connections suffice.

## What went well
- Burn-rate alert detected the issue in 3 minutes.
- Rollback path was clean and fast once the cause was found.

## What went wrong / where we got lucky
- Staging load was too low to surface pool exhaustion.
- The config default change wasn't flagged in review.

## Action items
| Action | Owner | Priority | Due | Tracking |
|--------|-------|----------|-----|----------|
| Add load test at prod-like concurrency to CI gate | Ayushi | P1 | 2026-02-01 | #1421 |
| Fail fast on missing pool config (no silent default) | payments team | P1 | 2026-01-25 | #1422 |
| Alert on active DB connections vs pool max | SRE | P2 | 2026-02-08 | #1423 |
