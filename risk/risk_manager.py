import logging

class RiskManager:

    def __init__(self, max_positions=3, risk_per_trade=0.01):
        self.max_positions = max_positions
        self.risk_per_trade = risk_per_trade

    def can_open_positions(self, open_trades):
        return len(open_trades) < self.max_positions
    
    def calculate_position_size(self, balance, entry_price, stop_loss):
        risk_amount = balance * self.risk_per_trade #ejemplo: 10000 * 0.01 = $100

        sl_distance = abs(entry_price - stop_loss) # ejemplo: 0.0015

        if sl_distance == 0:
            logging.warning("SL distance is 0, skipping position size calc")
            return 0
        
        #convertir distancia a pips (1 pip = 0.0001 en pares de 4 decimales)
        sl_pips = sl_distance / 0.0001 # ejempo: 0.0015 / 0.0001 = 15 pips

        #valor de 1 pip por lote estanndar (100,000 unidades) en pares XXX/USD
        pip_value_per_lot = 10

        #size en lotes
        size_lots = risk_amount / (sl_pips * pip_value_per_lot) # 100 / (15 * 10) = 0.67 lotes

        #limitar a maximo 2 lotes, por seguridad
        max_lots = 2
        size_lots = min(size_lots, max_lots)

        #redondear a 2 decimales (precision estandar en los brokers)
        size_lots = round(size_lots, 2)

        logging.info(f"Position size: {size_lots} lots | SL: {sl_pips:.1f} pips | Risk ${risk_amount:.2f}")

        return size_lots