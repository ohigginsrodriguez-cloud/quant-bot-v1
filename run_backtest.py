import logging
import sys

from config.settings import create_directories, LOG_DIR
from data.data_loader import load_data
from strategies.volatility_strategy import VolatilityStrategy
from strategies.volatility_config import PARAMS
from backtest.engine import BacktestEngine
from backtest.report import print_report
from backtest.simulator import STOCK, FOREX, CRYPTO, INDEX

create_directories()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "backtest.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# CONFIGURACION
# argumentos opcionales: symbol, period, timeframe
SYMBOL    = sys.argv[1] if len(sys.argv) > 1 else 'EURUSD=X'
PERIOD    = sys.argv[2] if len(sys.argv) > 2 else '2y'
TIMEFRAME = sys.argv[3] if len(sys.argv) > 3 else '4h'
MARKET    = sys.argv[4] if len(sys.argv) > 4 else FOREX
WARMUP    = 100

logging.info(f"Loading data: {SYMBOL} | {PERIOD} | {TIMEFRAME}")
data = load_data(SYMBOL, PERIOD, TIMEFRAME)

if data is None or data.empty:
    logging.error("Could not load data")
    sys.exit(1)

logging.info(f"Candles loaded: {len(data)}")

strategy = VolatilityStrategy(PARAMS)
engine = BacktestEngine(strategy, initial_balance=10000, warmup=WARMUP, market_type=MARKET)

logging.info("Running backtest...")
metrics, closed_trades = engine.run(data)

print_report(metrics, closed_trades)