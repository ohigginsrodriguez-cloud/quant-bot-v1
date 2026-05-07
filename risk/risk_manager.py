class RiskManager:

    def __init__(self, max_positions=3):
        self.max_positions = max_positions

    def can_open_positions(self, open_trades):
        return len(open_trades) < self.max_positions