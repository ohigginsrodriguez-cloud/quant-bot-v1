from core.signals import BUY, SELL, HOLD
from core.positions import LONG, SHORT

class BacktestSimulator:


    def __init__(self,  initial_balance=10000, risk_per_trade=0.01, max_positions=3):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.risk_per_trade = risk_per_trade
        self.max_positions = max_positions
        self.open_trades = []
        self.closed_trades =[]


        def _calculate_pnl(self, side, entry, exit_price, size):
            pips = (exit_price - entry) / 0.0001

            if side == SHORT:
                pips = -pips
                return round(pips * 10 * size, 2)
            
        def _calculate_position_size(self, price, stop_loss):
            risk_amount = self.balance * self.risk_per_trade
            sl_pips = abs(price - stop_loss) / 0.0001

            if sl_pips == 0:
                return 0
            
            size = risk_amount / (sl_pips * 10)
            return round(min(size, 2), 2)
        
        def _close_trade(self, trade, exit_price, reason):
            pnl = self._calculate_pnl(trade['side'], trade['entry_price'], exit_price, trade['size'])
            trade['exit_price'] = exit_price
            trade['pnl'] = pnl
            trade['reason'] = reason
            self.closed_trades.append(trade)
            self.balance += pnl
            self.open_trades.remove(trade)

        def step(self, signal, price, stop_loss, take_profit, atr, timestamp):

            # REVISAR TRADES ABIERTOS
            for trade in list(self.open_trades):
                side = trade['side']

                # TRAILING STOP
                trail = atr * 1.5
                if side == LONG:
                    new_sl = price - trail
                    if trade['stop_loss'] is None or new_sl > trade['stop_loss']:
                        trade['stop_loss'] = new_sl
                elif side == SHORT:
                    new_sl = price + trail
                    if trade['stop_loss'] is None or new_sl < trade['stop_loss']:
                        trade['stop_loss'] = new_sl

                # CHECK SL
                if trade['stop_loss'] is not None:
                    if side == LONG and price <= trade['stop_loss']:
                        self._close_trade(trade, price, 'SL')
                        continue
                    if side == SHORT and price >= trade['stop_loss']:
                        self._close_trade(trade, price, 'SL')
                        continue

                # CHECK TP
                if trade['take_profit'] is not None:
                    if side == LONG and price >= trade['take_profit']:
                        self._close_trade(trade, price, 'TP')
                        continue
                    if side == SHORT and price <= trade['take_profit']:
                        self._close_trade(trade, price, 'TP')
                        continue

                # REVERSAL
                if side == LONG and signal == SELL:
                    self._close_trade(trade, price, 'REVERSAL')
                elif side == SHORT and signal == BUY:
                    self._close_trade(trade, price, 'REVERSAL')

            # ABRIR NUEVO TRADE
            if signal == HOLD or stop_loss is None:
                return

            if len(self.open_trades) >= self.max_positions:
                return

            # NO ABRIR EN MISMO SIMBOLO SI YA HAY TRADE
            size = self._calculate_position_size(price, stop_loss)

            if size == 0:
                return

            if signal == BUY:
                self.open_trades.append({
                    'side': LONG,
                    'entry_price': price,
                    'size': size,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'entry_time': timestamp
                })

            elif signal == SELL:
                self.open_trades.append({
                    'side': SHORT,
                    'entry_price': price,
                    'size': size,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'entry_time': timestamp
                })