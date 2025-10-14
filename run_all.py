import subprocess
import threading
import signal
import os
import sys

processes = []

def run_process(command):
    env = os.environ.copy()
    env["USE_GUNICORN"] = "1"

    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        preexec_fn=os.setsid,
        env=env
    )
    processes.append(process)
    for line in process.stdout:
        print(line, end='')
    process.wait()

def terminate_processes(signum, frame):
    print("\n[!] stopping all processes...")
    for p in processes:
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGINT)
        except Exception:
            pass
    sys.exit(0)

signal.signal(signal.SIGINT, terminate_processes)

commands = [
    "python3 init_db.py",
    "python3 -m analytics_api",
    "python3 dashboard/app.py"
]

threads = []
for cmd in commands:
    t = threading.Thread(target=run_process, args=(cmd,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
