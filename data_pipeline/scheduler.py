
from __future__ import absolute_import

from data_pipeline.logger import Logger
import time
import schedule

class Scheduler(object):

    def __init__(self, interval_in_secs, job, *job_args):
        self.interval = interval_in_secs
        self.scheduler = schedule.Scheduler()
        self.scheduler.every(interval_in_secs).seconds.do(job, *job_args)

    def run(self):
        while True:
            self.scheduler.run_pending()
            time.sleep(self.interval)