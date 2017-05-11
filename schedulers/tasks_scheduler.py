import os
from datetime import datetime
import subprocess

from apscheduler.schedulers.blocking import BlockingScheduler

import sc_localsettings

def tick():
    print('Tick! The time is: %s' % datetime.now())
    subprocess.call(['python', sc_localsettings.SCHEDULER_SCRIPT1])


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(tick, 'interval', seconds=sc_localsettings.SCHEDULER_SLEEP_SECONDS)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
