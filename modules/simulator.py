import threading, time, random

SSH_FAILS = [
    "Failed password for invalid user root from 192.168.1.100 port 22 ssh2",
    "Failed password for admin from 192.168.1.101 port 22 ssh2",
    "Failed password for test from 10.0.0.23 port 22 ssh2",
]
OK_LINES = [
    "Accepted password for user1 from 192.168.1.55 port 22 ssh2",
    "systemd[1]: Started Daily apt download activities.",
    "cron[2033]: (root) CMD (  cd / && run-parts --report /etc/cron.hourly)"
]
SENSITIVE = [
    "GET /etc/passwd HTTP/1.1",
    "GET /wp-admin HTTP/1.1",
    "GET /.git/config HTTP/1.1"
]

def _writer(path):
    while True:
        bucket = random.choices([SSH_FAILS, OK_LINES, SENSITIVE], weights=[4,4,2])[0]
        line = random.choice(bucket)
        ts = time.strftime("%b %d %H:%M:%S")
        host = "server"
        out = f"{ts} {host} app[1234]: {line}\n"
        with open(path, "a") as f:
            f.write(out)
        time.sleep(random.uniform(0.4, 1.5))

def start_simulator(path="logs/sample_syslog.log"):
    t = threading.Thread(target=_writer, args=(path,), daemon=True)
    t.start()
