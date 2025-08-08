import json, time
from datetime import datetime
from collections import defaultdict

class Reporter:
    def __init__(self, log_path="output/alerts.log", json_path="output/alerts.jsonl"):
        self.log_path = log_path
        self.json_path = json_path
        self.stats = defaultdict(int)

    def alert(self, kind, message, meta=None):
        ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        line = f"[{ts}] [{kind}] {message}"
        with open(self.log_path,"a") as f:
            f.write(line + "\n")
        rec = {"ts": ts, "kind": kind, "message": message, "meta": meta or {}}
        with open(self.json_path,"a") as f:
            f.write(json.dumps(rec) + "\n")
        self.stats[kind] += 1

    def summary(self):
        total = sum(self.stats.values())
        by_kind = ", ".join(f"{k}:{v}" for k,v in self.stats.items()) or "none"
        return f"Summary -> total alerts: {total} ({by_kind})"
