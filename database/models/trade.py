class Trade:
    def __init__(self, symbol, action, price, timestamp, status="OPEN"):
        self.symbol = symbol
        self.action = action
        self.price = price
        self.timestamp = timestamp
        self.status = status