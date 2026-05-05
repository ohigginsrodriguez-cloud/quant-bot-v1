from data.data_loader import load_data
from data.data_processor import process_data
from config.settings import SYMBOL, PERIOD, TIMEFRAME

data = load_data(SYMBOL, PERIOD, TIMEFRAME)

if data is None:
    print('No se pudieron cargar los datos')
else:
    data = process_data(data)
    print(data.tail())
    print(data.columns)