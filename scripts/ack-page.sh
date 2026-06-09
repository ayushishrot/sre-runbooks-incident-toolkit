#!/usr/bin/env bash
# Acknowledge a PagerDuty incident from the CLI during on-call triage.
# Usage: PD_TOKEN=... PD_FROM=you@example.com ./ack-page.sh <incident_id>
set -euo pipefail

INCIDENT_ID="${1:?usage: ack-page.sh <incident_id>}"
: "${PD_TOKEN:?PD_TOKEN (PagerDuty API token) is required}"
: "${PD_FROM:?PD_FROM (your PagerDuty login email) is required}"

curl -sf -X PUT "https://api.pagerduty.com/incidents/${INCIDENT_ID}" \
  -H "Authorization: Token token=${PD_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "From: ${PD_FROM}" \
  -d '{"incident":{"type":"incident_reference","status":"acknowledged"}}' \
  >/dev/null

echo "Acknowledged incident ${INCIDENT_ID}."
