import logging
from core.positions import LONG, SHORT

class Exitmanager:

    def _calculate_pnl(self, side, entry, exit_price, size):
        pips = (exit_price - entry) / 0.0001

        if side == SHORT:
            pips = -pips

        pnl = pips * 10 * size
        return round(pnl, 2)
    
    def check_exit(self, trade, price):
        side = trade['side']
        entry = trade['entry_price']
        size = trade['size']
        sl =  trade['stop_loss']
        tp = trade['take_profit']

        #STOP LOSS
        if sl is not None:
            if side == LONG and price <= sl:
                pnl = self._calculate_pnl(LONG, entry, price, size)
                return "SL", pnl
            
            if side == SHORT and price >= sl:
                pnl = self._calculate_pnl(SHORT, entry, price, size)
                return "SL", pnl
            
        #TAKE PROFIT
        if tp is not None:
            if side == LONG and price >= tp:
                pnl = self._calculate_pnl(LONG, entry, price, size)
                return "TP", pnl
            
            if side == SHORT and price <= tp:
                pnl = self._calculate_pnl(SHORT, entry, price, size)
                return "TP", pnl
            
        return None, None
    
    def update_trailing_stop(self, trade, price, atr):
        side = trade['side']
        current_sl = trade['stop_loss']

        #trailing de 1.5x ATR - se adapta a la volatilidad actual
        trail_distance = atr * 1.5

        if side == LONG:
            new_sl_candidate = price - trail_distance

            if current_sl is None:
                return new_sl_candidate
            
            return max(current_sl, new_sl_candidate)
        
        if side == SHORT:
            new_sl_candidate = price + trail_distance

            if current_sl is None:
                return new_sl_candidate
            
            return min(current_sl, new_sl_candidate)