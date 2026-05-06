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
    logging.warning('No se pudieron cargar los datos')
    exit()

data = process_data(data, PARAMS)

if data is None or data.empty:
        logging.warning("No hay datos suficientes para estrategia")
        exit()

logging.info(f"Data length after processing: {len(data)}")

strategy = VolatilityStrategy(PARAMS)

executor = Executor()
engine = TradingEngine(strategy, executor)
signal = engine.run(data)

logging.info(f"Signal generated: {signal}")

print(data.tail())
print(f"Signal: {signal}")