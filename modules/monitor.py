import time, os, sys
from modules.config import load_config
from modules.detector import Detector
from modules.reporter import Reporter

def tail_follow(fp):
    fp.seek(0, os.SEEK_END)
    while True:
        line = fp.readline()
        if not line:
            time.sleep(0.25)
            continue
        yield line

def monitor_log(path, summary_every=60):
    cfg = load_config()
    reporter = Reporter()
    detector = Detector(cfg, reporter)

    print(f"🔍 Monitoring {path} ... (summary every {summary_every}s)")
    last_summary = time.time()
    with open(path, "r") as f:
        for line in tail_follow(f):
            detector.process_line(line)
            if summary_every and (time.time() - last_summary) >= summary_every:
                print(reporter.summary())
                last_summary = time.time()
