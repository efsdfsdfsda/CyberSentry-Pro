import json

DEFAULT_CONFIG = {
    "suspicious_keywords": ["unauthorized", "failed login", "malicious", "root access", "attack"],
    "sensitive_paths": ["/etc/passwd", "/admin", "/wp-admin", "/.git"],
    "ssh_brute_force": {
        "regex": r"Failed password for .* from (?P<ip>(?:\d{1,3}\.){3}\d{1,3})",
        "threshold": 3,
        "window_seconds": 120
    },
    "whitelist_ips": ["127.0.0.1"],
    "max_url_length": 150
}

def load_config(path="config.json"):
    try:
        with open(path,"r") as f:
            data = json.load(f)
            # shallow merge with defaults
            cfg = DEFAULT_CONFIG.copy()
            cfg.update(data)
            return cfg
    except FileNotFoundError:
        return DEFAULT_CONFIG
