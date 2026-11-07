"""Compute simple DORA metrics from a GitHub Actions runs JSON file."""
import json
import statistics
import sys
from datetime import datetime, timedelta, timezone

DAYS = 30


def parse(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def hours(delta):
    return round(delta.total_seconds() / 3600, 2)


def main(path):
    with open(path) as handle:
        runs = json.load(handle)["workflow_runs"]
    since = datetime.now(timezone.utc) - timedelta(days=DAYS)
    runs = [r for r in runs if parse(r["created_at"]) >= since]
    runs = [r for r in runs if r["conclusion"] in ("success", "failure")]
    runs.sort(key=lambda r: r["created_at"])
    good = [r for r in runs if r["conclusion"] == "success"]
    bad = [r for r in runs if r["conclusion"] == "failure"]

    lead = [
        parse(r["updated_at"]) - parse(r["head_commit"]["timestamp"])
        for r in good
    ]
    recovery = []
    for failed in bad:
        later = [
            r for r in good
            if parse(r["created_at"]) > parse(failed["created_at"])
        ]
        if later:
            recovery.append(
                parse(later[0]["updated_at"]) - parse(failed["created_at"])
            )

    total = len(runs)
    rate = round(100 * len(bad) / total, 1) if total else 0
    print(f"## DORA metrics (last {DAYS} days)")
    print()
    print("| Metric | Value |")
    print("|---|---|")
    print(f"| Deployment frequency | {len(good)} in {DAYS} days |")
    if lead:
        print(f"| Lead time (median) | {hours(statistics.median(lead))} h |")
    print(f"| Change failure rate | {rate}% |")
    if recovery:
        avg = sum(recovery, timedelta()) / len(recovery)
        print(f"| Mean time to recovery | {hours(avg)} h |")


if __name__ == "__main__":
    main(sys.argv[1])
