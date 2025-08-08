import re, time
from collections import deque, defaultdict

class Detector:
    def __init__(self, cfg, reporter):
        self.cfg = cfg
        self.reporter = reporter
        self.ssh_re = re.compile(cfg["ssh_brute_force"]["regex"])
        self.fail_window = cfg["ssh_brute_force"]["window_seconds"]
        self.fail_threshold = cfg["ssh_brute_force"]["threshold"]
        self.fail_events = defaultdict(deque)  # ip -> deque[timestamps]

    def _within_window(self, dq, now):
        while dq and now - dq[0] > self.fail_window:
            dq.popleft()

    def process_line(self, line):
        l = line.strip()
        ll = l.lower()
        now = time.time()

        # Whitelist skip
        for ip in self.cfg.get("whitelist_ips", []):
            if ip and ip in l:
                return False

        fired = False

        # Keywords
        for kw in self.cfg["suspicious_keywords"]:
            if kw in ll:
                self.reporter.alert("keyword", f"Suspicious keyword '{kw}' in line: {l[:200]}", {"keyword": kw})
                fired = True
                break

        # Sensitive paths
        if not fired:
            for p in self.cfg["sensitive_paths"]:
                if p in l:
                    self.reporter.alert("sensitive-path", f"Access to sensitive path '{p}' -> {l[:200]}", {"path": p})
                    fired = True
                    break

        # SSH brute force
        m = self.ssh_re.search(l)
        if m:
            ip = m.group("ip")
            dq = self.fail_events[ip]
            self._within_window(dq, now)
            dq.append(now)
            if len(dq) >= self.fail_threshold:
                self.reporter.alert("ssh-bruteforce", f"{len(dq)} failed SSH logins from {ip} within {self.fail_window}s", {"ip": ip, "count": len(dq)})
                dq.clear()
            else:
                self.reporter.alert("ssh-fail", f"Failed SSH login from {ip}", {"ip": ip})
            fired = True

        return fired
