from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from services import generate_billing
from datetime import datetime

def semester_cron_job():
    """
    Cron job that runs at the start of each semester
    """
    print(f"Running semester billing generation at {datetime.now()}")
    try:
        billings_created = generate_billing()
        print(f"Successfully created {billings_created} billings")
    except Exception as e:
        print(f"Error in billing generation: {str(e)}")

def setup_scheduler():
    """
    Set up APScheduler with cron jobs
    """
    scheduler = BackgroundScheduler()

    # Run at the start of each semester
    # Semester 1: July 1st at 00:00
    # Semester 2: January 1st at 00:00
    semester_trigger = CronTrigger(
        month='1,7',  # January and July
        day=1,
        hour=0,
        minute=0
    )

    scheduler.add_job(
        semester_cron_job,
        trigger=semester_trigger,
        id='semester_billing',
        name='Generate Semester Billings',
        replace_existing=True
    )

    return scheduler

def start_scheduler():
    """
    Start the scheduler
    """
    scheduler = setup_scheduler()
    scheduler.start()
    print("Scheduler started successfully")
    return scheduler

def stop_scheduler(scheduler):
    """
    Stop the scheduler
    """
    if scheduler:
        scheduler.shutdown()
        print("Scheduler stopped")
