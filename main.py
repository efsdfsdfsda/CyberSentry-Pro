import argparse
from modules.monitor import monitor_log
from modules.simulator import start_simulator

def parse_args():
    p = argparse.ArgumentParser(description="CyberSentry - Suspicious Activity Monitoring")
    p.add_argument("--log", default="logs/sample_syslog.log", help="Path to log file to monitor")
    p.add_argument("--simulate", action="store_true", help="Append simulated events to the log while monitoring")
    p.add_argument("--summary-every", type=int, default=60, help="Print summary stats every N seconds (0 disables)")
    return p.parse_args()

def main():
    args = parse_args()
    if args.simulate:
        start_simulator(args.log)
    monitor_log(args.log, summary_every=args.summary_every)

if __name__ == "__main__":
    main()
