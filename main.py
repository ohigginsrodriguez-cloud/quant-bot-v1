import logging
import sys

from config.settings import LOG_DIR, create_directories, SYMBOL, PERIOD, TIMEFRAME
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

def setup_logging(log_file="bol_log"):
    create_directories()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_DIR / log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

def build_bot():
    init_db()
    account = Account(initial_balance=10000)
    strategy = VolatilityStrategy(PARAMS)
    risk_manager = RiskManager()
    repository = TradeRepository()
    exit_manager = Exitmanager()
    executor = Executor(repository, risk_manager, account, exit_manager)
    engine = TradingEngine(strategy, risk_manager, executor, repository)
    return engine, account

def run_bot(engine, account):
    data = load_data(SYMBOL, PERIOD, TIMEFRAME)

    if data is None or data.empty:
        logging.warning("Data could not be loaded, skipping")
        return None
    
    signal = engine.run(data, SYMBOL)
    logging.info(f"Signal: {signal} | Balance: ${account.balance:.2f}")
    return signal

if __name__ == "__main__":
    setup_logging("bot.log")
    engine, account = build_bot()
    run_bot(engine, account)