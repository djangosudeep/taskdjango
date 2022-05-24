from apscheduler.schedulers.background import BackgroundScheduler
from . import update

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update.aptask, 'interval', hours = 24)

    scheduler.start()