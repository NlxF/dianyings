from django_cron import cronScheduler, Job
from models import updatehot10everynanjing


class UpdateHot(Job):
    """run every 24h"""
    run_every = 6

    def job(self):
        """此函数每24小时调用一次"""
        updatehot10everynanjing()

cronScheduler.register(UpdateHot)