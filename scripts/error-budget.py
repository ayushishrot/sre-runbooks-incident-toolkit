#!/usr/bin/env python3
"""Compute remaining error budget for a service over a 30-day window.

Reads the success ratio from Prometheus and compares it to the SLO target.

Usage:
    PROM_URL=http://prometheus:9090 ./error-budget.py <service> <target_pct>
Example:
    PROM_URL=http://prometheus:9090 ./error-budget.py orders 99.9
"""
import json
import os
import sys
import urllib.parse
import urllib.request

WINDOW = "30d"


def query(prom_url: str, expr: str) -> float:
    url = f"{prom_url}/api/v1/query?" + urllib.parse.urlencode({"query": expr})
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.load(resp)
    result = data["data"]["result"]
    if not result:
        raise SystemExit(f"no data for query: {expr}")
    return float(result[0]["value"][1])


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    service, target_pct = sys.argv[1], float(sys.argv[2])
    prom_url = os.environ.get("PROM_URL")
    if not prom_url:
        raise SystemExit("PROM_URL is required")

    expr = (
        f'sum(rate(http_requests_total{{job="{service}",code!~"5.."}}[{WINDOW}]))'
        f' / sum(rate(http_requests_total{{job="{service}"}}[{WINDOW}]))'
    )
    sli = query(prom_url, expr)

    slo = target_pct / 100.0
    budget = 1.0 - slo                       # allowed unavailability
    consumed = max(0.0, slo - sli)           # how far below target we are
    remaining_frac = 1.0 if budget == 0 else max(0.0, 1.0 - consumed / budget)
    minutes_total = budget * 30 * 24 * 60
    minutes_left = remaining_frac * minutes_total

    print(f"service:           {service}")
    print(f"window:            {WINDOW}")
    print(f"SLI (success):     {sli * 100:.4f}%")
    print(f"SLO target:        {target_pct:.4f}%")
    print(f"budget remaining:  {remaining_frac * 100:.1f}%  (~{minutes_left:.0f} min of {minutes_total:.0f})")

    if remaining_frac < 0.1:
        print("STATUS: <10%  feature freeze per error-budget policy")
        return 1
    print("STATUS: healthy")
    return 0


if __name__ == "__main__":
    sys.exit(main())
