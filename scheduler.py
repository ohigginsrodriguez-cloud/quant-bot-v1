import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from config.settings import SYMBOL, SCHEDULER_INTERVAL
from main import setup_logging, build_bot, run_bot

setup_logging("scheduler.log")

engine, account = build_bot()

def job():
    logging.info(f"--- Scheduler run | {SYMBOL} ---")
    run_bot(engine, account)

if __name__ == "__main__":
    scheduler = BlockingScheduler()

    scheduler.add_job(
        job, 
        trigger=IntervalTrigger(hours=SCHEDULER_INTERVAL),
        id="trading_bot",
        name=f"Trading bot {SYMBOL}",
        replace_existing=True
    )

    logging.info(f"Scheduler started | Interval: {SCHEDULER_INTERVAL}h | Symbol: {SYMBOL}")
    logging.info("Press Ctrl+C to stop")

    run_bot(engine, account) # correr inmediatamente sin esperar primer intervalo

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logging.info("Scheduler stopped")
        scheduler.shutdown()