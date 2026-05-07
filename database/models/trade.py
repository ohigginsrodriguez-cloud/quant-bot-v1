class Trade:
    def __init__(self, symbol, side, size, entry_price, entry_timestamp, status="OPEN", 
                 exit_price=None, exit_timestamp=None, pnl=None):
        self.symbol = symbol
        self.side = side        #LONG o SHORT
        self.size = size
        self.entry_price = entry_price
        self.entry_timestamp = entry_timestamp
        self.status = status
        self.exit_price = exit_price
        self.exit_timestamp = exit_timestamp
        self.pnl = pnl