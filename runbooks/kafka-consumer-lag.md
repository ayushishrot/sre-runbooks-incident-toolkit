# Runbook: Kafka Consumer Lag

**Trigger:** `KafkaConsumerLagHigh` — a consumer group's lag exceeds threshold and is
growing (Confluent Kafka on Kubernetes).

## 1. Scope it
- Grafana → *Confluent Kafka on k8s* dashboard → "Consumer lag by group".
- Or CLI: `PROM_URL=... ./scripts/kafka-lag-top.sh` to rank groups by lag.
- Lag growing or flat? Flat-but-high after a spike often self-recovers; growing lag needs action.

## 2. Decide: consumer-side or broker-side
| Signal | Cause | Move |
|--------|-------|------|
| One group lags, brokers healthy | Slow/crashed consumers | Check consumer pods (CrashLoop? OOM?), scale replicas up to ≤ partition count |
| All groups lag, broker CPU/disk high | Broker saturation | Check broker resources, under-replicated partitions; add capacity |
| Lag on specific partitions | Hot partition / skewed key | Review partitioning key; rebalance |
| Lag after deploy | Poison message / slow processing | Roll back consumer, inspect DLQ |

## 3. Fast levers
- **Scale consumers** (cannot exceed partition count for parallelism).
- **Check under-replicated partitions:** `kafka_server_replicamanager_underreplicatedpartitions > 0` indicates broker trouble.
- **Pause non-critical producers** to let consumers catch up if the topic is backed up.

## 4. Resolve
Lag returning to baseline and trending down. If processing was the bottleneck, file an
action item to right-size partitions/consumers.
