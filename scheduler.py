import logging
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from config.settings import LOG_DIR, create_directories, SYMBOL, PERIOD, TIMEFRAME, SCHEDULER_INTERVAL
from data.data_loader import load_data
from strategies.volatility_strategy import VolatilityStrategy
from strategies.volatility_config import PARAMS
from core.engine import TradingEngine
from execution.executor import Executor
from database.db import init_db
from database.repository.trade_repository import TradeRepository
from risk.risk_manager import RiskManager
from portfolio.account import Account
from core.exit_manager import Exitmanager

create_directories()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "scheduler.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

init_db()

#inicializar componentes una sola vez
account = Account(initial_balance=10000)
strategy = VolatilityStrategy(PARAMS)
risk_manager = RiskManager()
repository = TradeRepository()
exit_manager = Exitmanager()
executor = Executor(repository, risk_manager, account, exit_manager)
engine = TradingEngine(strategy, risk_manager, executor, repository)

def run_bot():
    logging.info(f"--- Running bot | {SYMBOL} | {TIMEFRAME} ---")

    data = load_data(SYMBOL, PERIOD, TIMEFRAME)

    if data is None or data.empty:
        logging.warning("Data could not be loaded, skipping this run")
        return
    
    try:
        signal = engine.run(data, SYMBOL)
        logging.info(f"Signal: {signal} | Balance: ${account.balance:.2f}")
    except Exception as e:
        logging.error(f"Bot error: {e}", exc_info=True)


if __name__ == "__main__":
    scheduler = BlockingScheduler()

    scheduler.add_job(
        run_bot,\
        trigger=IntervalTrigger(hours=SCHEDULER_INTERVAL),
        id="trading_bot",
        name=f"Trading bot {SYMBOL}",
        replace_existing=True
    )

    logging.info(f"Scheduler started | Interval: {SCHEDULER_INTERVAL}h | Symbol: {SYMBOL}")
    logging.info("Press Crtl+C to stop")

    #correr inmediatamente al iniciar, sin esperar el primer intervalo

    run_bot()

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logging.info("Scheduler stopped")
        scheduler.shutdown()