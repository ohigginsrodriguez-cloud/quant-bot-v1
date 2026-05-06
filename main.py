import logging
import sys

from config.settings import LOG_DIR
from data.data_loader import load_data
from data.data_processor import process_data
from config.settings import SYMBOL, PERIOD, TIMEFRAME
from strategies.volatility_strategy import VolatilityStrategy
from strategies.volatility_config import PARAMS
from core.engine import TradingEngine
from execution.executor import Executor
from database.db import init_db
from database.repository.trade_repository import TradeRepository

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

data = process_data(data, PARAMS)

if data is None or data.empty:
        logging.warning("There is not enough data for the strategy")
        exit()

strategy = VolatilityStrategy(PARAMS)

init_db()

repository = TradeRepository()
executor = Executor(repository)

engine = TradingEngine(strategy, executor, repository)
signal = engine.run(data, SYMBOL)

logging.info(f"\n{data.tail()}")
logging.info(f"Signal: {signal}")