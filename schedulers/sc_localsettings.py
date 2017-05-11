import os

SCHEDULER_SLEEP_SECONDS = 10

BASE_DIR = os.path.dirname(__file__)
SCHEDULER_SCRIPT1 = "%s%s%s" % (BASE_DIR, os.sep, "../api_emulator"+os.sep+"api_sample_loop1.py")
THREADED_SCHEDULER_QUEUE_PROBE_COUNT = 10           # Enter 0 for infinite scheduler loop
THREADED_SCHEDULER_SLEEP_TIME = 10

