from pathlib import Path
import os

#__file__ es la ruta del archivo
# .resolve la convierte en absoluta para evitar errores
# .parent va un espacio atras en carpetas
BASE_DIR = Path(__file__).resolve().parent.parent # BASE DIRECTORY (RAIZ DEL PROYECTO)

# para unir rutas solo usamos un "/" y el nombre del dir
# PATHS
DB_PATH = BASE_DIR / "database" / "trades.db"
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

def create_directories():
    # mkdir para crear la carpeta 
    # exit_ok=True para que no de error si ya existe
    LOG_DIR.mkdir(parents=True ,exist_ok=True) # parents=True crea la ruta si falta algo

# os.getenv() para variables de entorno
# TRADING CONFIG
SYMBOL = os.getenv('SYMBOL', 'EURUSD=X')
TIMEFRAME = os.getenv('TIMEFRAME', '4h')
PERIOD = os.getenv('PERIOD', '3mo')
STRATEGY_NAME = os.getenv('STRATEGY_NAME', 'volatility')

# int para transformar e intervalo de string a int
# SCHEDULER (EN HORAS)
SCHEDULER_INTERVAL = int(os.getenv('SCHEDULER_INTERVAL', 1))
if SCHEDULER_INTERVAL <= 0:
    raise ValueError("SCHEDULER_INTERVAL must be > 0")
