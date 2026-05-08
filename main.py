import logging
import sys

from config.settings import LOG_DIR, create_directories
from data.data_loader import load_data
from config.settings import SYMBOL, PERIOD, TIMEFRAME
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
          logging.FileHandler(LOG_DIR / "bot.log"),
          logging.StreamHandler(sys.stdout)
    ]
)

data = load_data(SYMBOL, PERIOD, TIMEFRAME)

if data is None or data.empty:
    logging.warning('Data could not be loaded')
    exit()

init_db()
account = Account(initial_balance=10000)
strategy = VolatilityStrategy(PARAMS)
risk_manager = RiskManager()
repository = TradeRepository()
exit_manager = Exitmanager()
executor = Executor(repository, risk_manager, account, exit_manager)
engine = TradingEngine(strategy, risk_manager, executor, repository)
signal = engine.run(data, SYMBOL)

logging.info(f"Signal: {signal}")