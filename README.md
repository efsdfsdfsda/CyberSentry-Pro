# 🛡️ CyberSentry pro – Suspicious Activity Monitoring

Real-time monitoring for system logs with configurable detection and summarized alerts.

## ✨ What's New
- Configurable rules (`modules/config.py` or `config.json`)
- SSH brute-force **threshold + time window**
- Sensitive path detection
- Keyword detection
- **JSONL + log** reporters with per-kind stats
- **Built-in simulator** to generate realistic events
- Periodic summary (configurable)

## 📦 Structure
```
CyberSentry/
  logs/sample_syslog.log
  modules/
    monitor.py
    detector.py
    config.py
    reporter.py
    simulator.py
  output/alerts.log
  output/alerts.jsonl
  main.py
  README.md
  requirements.txt
```

## ▶️ Run
```bash
python main.py --log logs/sample_syslog.log --simulate --summary-every 30
```

## 🧠 Customize
- Create a `config.json` next to `main.py` to override defaults from `modules/config.py`.
- Example:
```json
{
  "ssh_brute_force": { "threshold": 5, "window_seconds": 180 },
  "whitelist_ips": ["127.0.0.1", "10.0.0.1"]
}
```

## 📝 Output
- `output/alerts.log` – human readable
- `output/alerts.jsonl` – one JSON per line for ingestion into SIEM/dashboards
```

