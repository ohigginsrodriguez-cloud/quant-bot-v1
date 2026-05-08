from core.positions import LONG, SHORT

class Exitmanager:
    
    def check_exit(self, trade, price):
        side = trade['side']
        entry = trade['entry_price']
        size = trade['size']
        sl =  trade['stop_loss']
        tp = trade['take_profit']

        #STOP LOSS
        if sl is not None:
            if side == LONG and price <= sl:
                return "SL", (price - entry) * size
            
            if side == SHORT and price >= sl:
                return "SL", (entry - price) * size
            
        #TAKE PROFIT
        if tp is not None:
            if side == LONG and price >= tp:
                return "TP", (price - entry) * size
            
            if side == SHORT and price <= tp:
                return "TP", (entry - price) * size
            
        return None, None
    
    def update_trailing_stop(self, trade, price):
        side = trade['side']
        current_sl = trade['stop_loss']

        if side == LONG:
            new_sl_candidate = price - 0.001

            if current_sl is None:
                return new_sl_candidate
            
            return max(current_sl, new_sl_candidate)
        
        if side == SHORT:
            new_sl_candidate = price + 0.001

            if current_sl is None:
                return new_sl_candidate
            
            return min(current_sl, new_sl_candidate)