from backtest.simulator import BacktestSimulator, STOCK, FOREX
from core.signals import BUY, SELL, HOLD

def test_open_trade():
    sim = BacktestSimulator(market_type=STOCK)
    sim.step(BUY, 100.0, 105.0, 95.0, 90.0, 115.0, 1.0, "2024-01-01")
    assert len(sim.open_trades) == 1
    assert sim.open_trades[0]['side'] == 'LONG'

def test_sl_hit():
    sim = BacktestSimulator(market_type=STOCK)
    # abrir LONG
    sim.step(BUY, 100.0, 105.0, 95.0, 90.0, 115.0, 1.0, "2024-01-01")
    assert len(sim.open_trades) == 1
    # candle que toca el SL (low <= 90)
    sim.step(HOLD, 88.0, 92.0, 85.0, None, None, 1.0, "2024-01-02")
    assert len(sim.open_trades) == 0
    assert len(sim.closed_trades) == 1
    assert sim.closed_trades[0]['reason'] == 'SL'

def test_tp_hit():
    sim = BacktestSimulator(market_type=STOCK)
    sim.step(BUY, 100.0, 105.0, 95.0, 90.0, 115.0, 1.0, "2024-01-01")
    # candle que toca el TP (high >= 115)
    sim.step(HOLD, 112.0, 120.0, 108.0, None, None, 1.0, "2024-01-02")
    assert len(sim.open_trades) == 0
    assert sim.closed_trades[0]['reason'] == 'TP'

def test_no_trade_on_hold():
    sim = BacktestSimulator(market_type=STOCK)
    sim.step(HOLD, 100.0, 105.0, 95.0, None, None, 1.0, "2024-01-01")
    assert len(sim.open_trades) == 0

def test_balance_updates_on_close():
    sim = BacktestSimulator(initial_balance=10000, market_type=STOCK)
    sim.step(BUY, 100.0, 105.0, 95.0, 90.0, 115.0, 1.0, "2024-01-01")
    sim.step(HOLD, 112.0, 120.0, 108.0, None, None, 1.0, "2024-01-02")
    assert sim.balance != 10000, "Balance debe cambiar despues de cerrar trade"

if __name__ == "__main__":
    test_open_trade()
    test_sl_hit()
    test_tp_hit()
    test_no_trade_on_hold()
    test_balance_updates_on_close()
    print("All tests passed")