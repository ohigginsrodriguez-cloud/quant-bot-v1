import json
import logging
from datetime import datetime, UTC
from config.settings import LOG_DIR

TRADES_LOG_DIR = LOG_DIR / "trades"

def log_trade(trade_data: dict):
    try:
        TRADES_LOG_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        symbol = trade_data.get("symbol", "UNKNOWN").replace("=", "")
        filename = f"{timestamp}_{symbol}_{trade_data.get('reason', 'TRADE')}.json"

        filepath = TRADES_LOG_DIR / filename

        with open(filepath, "w") as f:
            json.dump(trade_data, f, indent=2, default=str)

        logging.info(f"Audit log saved: {filename}")

    except Exception as e:
        logging.error(f"Failed to write audit audit log: {e}")