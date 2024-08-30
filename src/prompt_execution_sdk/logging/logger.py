import json
import time
import os
from threading import Lock


class Logger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.lock = Lock()

    def log(self, event: dict):
        with self.lock:
            timestamp = int(time.time())
            filename = f"{self.log_dir}/promptlogs_{timestamp}.json"
            with open(filename, 'a') as f:
                json.dump(event, f)
                f.write('\n')
