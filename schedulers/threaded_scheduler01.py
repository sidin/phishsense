import os
from datetime import datetime
import time
import subprocess

from threading import Timer

import sc_localsettings

def invoke_workflow_via_scheduler():
    subprocess.call(['python', sc_localsettings.SCHEDULER_SCRIPT1])


def tick():
    print('Tick! The time is: %s' % datetime.now())
    Timer(5, invoke_workflow_via_scheduler, ()).start()
    time.sleep(sc_localsettings.THREADED_SCHEDULER_SLEEP_TIME)

if __name__ == '__main__':
    try:
        if sc_localsettings.THREADED_SCHEDULER_QUEUE_PROBE_COUNT is 0:
            while 1:
                tick()
        else:
            for i in range(sc_localsettings.THREADED_SCHEDULER_QUEUE_PROBE_COUNT):
                tick()
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    except (KeyboardInterrupt, SystemExit):
        pass

