class RiskManager:

    def __init__(self, max_positions=3, risk_per_trade=0.01):
        self.max_positions = max_positions
        self.risk_per_trade = risk_per_trade

    def can_open_positions(self, open_trades):
        return len(open_trades) < self.max_positions
    
    def calculate_position_size(self, balance, entry_price, stop_loss_price):
        risk_amount = balance * self.risk_per_trade
        risk_per_unit = abs(entry_price - stop_loss_price)

        if risk_per_unit == 0:
            return 0
        
        size = risk_amount / risk_per_unit

        max_size = balance * 10
        return min(size, max_size)