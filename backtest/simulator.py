from core.signals import BUY, SELL, HOLD
from core.positions import LONG, SHORT

# tipos de mercado soportados
FOREX = 'forex'
STOCK = 'stock'
CRYPTO = 'crypto'
INDEX = 'index'

MARKET_TYPES = [FOREX, STOCK, CRYPTO, INDEX]


class BacktestSimulator:

    def __init__(self, initial_balance=10000, risk_per_trade=0.01, max_positions=3,
                 market_type=FOREX, spread=1.5, commission=6.0, slippage=0.5):
        
        if market_type not in MARKET_TYPES:
            raise ValueError(f"market_type debe ser uno de {MARKET_TYPES}")

        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.risk_per_trade = risk_per_trade
        self.max_positions = max_positions
        self.market_type = market_type
        self.open_trades = []
        self.closed_trades = []

        # costos — significado cambia por mercado
        # forex:  spread en pips, commission por lote, slippage en pips
        # stock:  spread en %, commission por operacion en $, slippage en %
        # crypto: spread en %, commission en % del trade, slippage en %
        # index:  spread en puntos, commission por contrato, slippage en puntos
        self.spread = spread
        self.commission = commission
        self.slippage = slippage

    def _calculate_pnl(self, side, entry, exit_price, size):
        if self.market_type == FOREX:
            pips = (exit_price - entry) / 0.0001
            if side == SHORT:
                pips = -pips
            pnl = pips * 10 * size

        elif self.market_type in (STOCK, CRYPTO):
            pnl = (exit_price - entry) * size
            if side == SHORT:
                pnl = -pnl

        elif self.market_type == INDEX:
            # multiplier estandar SP500/NQ = $50 por punto
            pnl = (exit_price - entry) * size * 50
            if side == SHORT:
                pnl = -pnl

        return round(pnl, 2)

    def _calculate_costs(self, price, size):
        if self.market_type == FOREX:
            pip_cost = (self.spread + self.slippage) * 10 * size
            commission_cost = self.commission * size
            return round(pip_cost + commission_cost, 2)

        elif self.market_type == STOCK:
            # spread y slippage como % del precio
            entry_cost = price * size * (self.spread + self.slippage) / 100
            return round(entry_cost + self.commission, 2)

        elif self.market_type == CRYPTO:
            # todo como % del valor del trade
            trade_value = price * size
            return round(trade_value * (self.spread + self.slippage + self.commission) / 100, 2)

        elif self.market_type == INDEX:
            # spread y slippage en puntos, commission por contrato
            point_cost = (self.spread + self.slippage) * size * 50
            return round(point_cost + self.commission * size, 2)

        return 0

    def _calculate_position_size(self, price, stop_loss):
        risk_amount = self.balance * self.risk_per_trade

        if self.market_type == FOREX:
            sl_pips = abs(price - stop_loss) / 0.0001
            if sl_pips == 0:
                return 0
            size = risk_amount / (sl_pips * 10)
            return round(min(size, 2.0), 2)

        elif self.market_type == STOCK:
            sl_distance = abs(price - stop_loss)
            if sl_distance == 0:
                return 0
            size = risk_amount / sl_distance
            return round(size, 4)

        elif self.market_type == CRYPTO:
            sl_distance = abs(price - stop_loss)
            if sl_distance == 0:
                return 0
            size = risk_amount / sl_distance
            return round(size, 6)

        elif self.market_type == INDEX:
            sl_points = abs(price - stop_loss)
            if sl_points == 0:
                return 0
            size = risk_amount / (sl_points * 50)
            return round(min(size, 10.0), 2)

        return 0

    def _close_trade(self, trade, exit_price, reason):
        pnl = self._calculate_pnl(trade['side'], trade['entry_price'], exit_price, trade['size'])
        costs = trade['costs']
        net_pnl = round(pnl - costs, 2)

        trade['exit_price'] = exit_price
        trade['pnl'] = net_pnl
        trade['gross_pnl'] = pnl
        trade['reason'] = reason

        self.closed_trades.append(trade)
        self.balance += net_pnl
        self.open_trades.remove(trade)

    def step(self, signal, price, stop_loss, take_profit, atr, timestamp):

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

        size = self._calculate_position_size(price, stop_loss)
        if size == 0:
            return

        costs = self._calculate_costs(price, size)
        side = LONG if signal == BUY else SHORT

        self.open_trades.append({
            'side': side,
            'entry_price': price,
            'size': size,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'entry_time': timestamp,
            'costs': costs
        })