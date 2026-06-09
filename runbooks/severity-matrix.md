# Severity Matrix

| Sev | Definition | Examples | Response | Update cadence |
|-----|------------|----------|----------|----------------|
| **SEV1** | Critical: full outage or data loss on a Tier-0 service | Checkout down, auth broken, payments failing | Page IC + Ops immediately, all-hands | 30 min |
| **SEV2** | Major: significant degradation, partial outage, no workaround | High error rate on core API, one region down | Page on-call, declare incident | 60 min |
| **SEV3** | Minor: degraded but functional, workaround exists | Elevated latency, single non-critical feature broken | Ticket, handle in business hours | At resolution |
| **SEV4** | Low: cosmetic or no customer impact | Logging gap, flaky non-blocking alert | Backlog | None |

**When unsure, round up.** It is cheaper to downgrade a SEV2 than to under-respond to a
real SEV1. Severity can change as understanding improves  restate it explicitly when it does.
