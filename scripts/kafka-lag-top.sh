#!/usr/bin/env bash
# Rank Kafka consumer groups by total lag using kafka-exporter metrics in Prometheus.
# Usage: PROM_URL=http://prometheus:9090 ./kafka-lag-top.sh
set -euo pipefail

: "${PROM_URL:?PROM_URL is required}"
EXPR='sort_desc(sum by (consumergroup) (kafka_consumergroup_lag))'

curl -sf --get "${PROM_URL}/api/v1/query" --data-urlencode "query=${EXPR}" \
  | python3 -c '
import sys, json
data = json.load(sys.stdin)["data"]["result"]
if not data:
    print("no consumer lag metrics found"); sys.exit(0)
print(f"{\"consumer group\":40s} {\"lag\":>12s}")
for r in data:
    print(f"{r[\"metric\"].get(\"consumergroup\",\"?\"):40s} {int(float(r[\"value\"][1])):>12d}")
'
