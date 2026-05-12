from risk.risk_manager import RiskManager

def test_position_size_basic():
    rm = RiskManager(risk_per_trade=0.01)
    size = rm.calculate_position_size(10000, 1.2000, 1.1900)
    assert size > 0, "Size debe ser mayor a 0"
    assert size <= 2.0, "Size no debe exceder el maximo de 2 lotes"

def test_position_size_zero_sl():
    rm = RiskManager()
    size = rm.calculate_position_size(10000, 1.2000, 1.2000)
    assert size == 0, "Size debe ser 0 si SL == entry"

def test_can_open_positions():
    rm = RiskManager(max_positions=3)
    assert rm.can_open_positions([]) == True
    assert rm.can_open_positions([1, 2]) == True
    assert rm.can_open_positions([1, 2, 3]) == False

if __name__ == "__main__":
    test_position_size_basic()
    test_position_size_zero_sl()
    test_can_open_positions()
    print("All tests passed")