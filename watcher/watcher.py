import os
import time
import json
import requests
from datetime import datetime
from collections import deque

# Environment variables
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
ACTIVE_POOL = os.getenv("ACTIVE_POOL", "blue")
ERROR_RATE_THRESHOLD = float(os.getenv("ERROR_RATE_THRESHOLD", "2"))
WINDOW_SIZE = int(os.getenv("WINDOW_SIZE", "200"))
ALERT_COOLDOWN_SEC = int(os.getenv("ALERT_COOLDOWN_SEC", "300"))

# Shared log file path
LOG_FILE = "/var/log/nginx/access.log"

# Rolling window for error rate
rolling_window = deque(maxlen=WINDOW_SIZE)

# Last alert timestamps
last_failover_alert = 0
last_error_rate_alert = 0

def post_slack(message):
    if SLACK_WEBHOOK_URL:
        payload = {"text": message}
        try:
            requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
        except Exception as e:
            print(f"Failed to send Slack alert: {e}")

# Track active pool
active_pool = ACTIVE_POOL

def tail_log(file_path):
    """Tail the Nginx log file."""
    with open(file_path, "r") as f:
        # Go to the end of file
        f.seek(0,2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

def parse_log_line(line):
    try:
        return json.loads(line)
    except:
        return {}

for line in tail_log(LOG_FILE):
    data = parse_log_line(line)
    if not data:
        continue

    # Add to rolling window
    rolling_window.append(data)

    # Check failover
    current_pool = data.get("pool", active_pool)
    if current_pool != active_pool and (time.time() - last_failover_alert) > ALERT_COOLDOWN_SEC:
        msg = f"Failover detected: {active_pool} → {current_pool} at {datetime.now()}"
        post_slack(msg)
        active_pool = current_pool
        last_failover_alert = time.time()

    # Check error rate
    if len(rolling_window) == WINDOW_SIZE:
        error_count = sum(1 for r in rolling_window if str(r.get("upstream_status","")).startswith("5"))
        error_rate = (error_count / len(rolling_window)) * 100
        if error_rate > ERROR_RATE_THRESHOLD and (time.time() - last_error_rate_alert) > ALERT_COOLDOWN_SEC:
            msg = f"High error rate detected: {error_rate:.2f}% over last {WINDOW_SIZE} requests at {datetime.now()}"
            post_slack(msg)
            last_error_rate_alert = time.time()


