"""Batch task coordinator"""
import schedule
import time


def schedule_tasks():
    """Schedule recurring background tasks"""
    # TODO: Schedule deduplication every 5 minutes
    # TODO: Schedule SLA calculations every 15 minutes
    # TODO: Schedule score computations hourly
    
    # schedule.every(5).minutes.do(deduplicate_reports)
    # schedule.every(15).minutes.do(calculate_slas)
    # schedule.every().hour.do(compute_scores)
    
    pass


def run_scheduler():
    """Run the scheduler loop"""
    schedule_tasks()
    
    while True:
        schedule.run_pending()
        time.sleep(60)
