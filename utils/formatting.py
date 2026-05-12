from backtest.simulator import FOREX, STOCK, CRYPTO, INDEX


def format_price(price, market_type=FOREX):
    if market_type == FOREX:
        return f"{price:.5f}"
    elif market_type == STOCK:
        return f"${price:.2f}"
    elif market_type == CRYPTO:
        return f"{price:.8f}"
    elif market_type == INDEX:
        return f"{price:.2f} pts"
    return f"{price}"


def format_size(size, market_type=FOREX):
    if market_type == FOREX:
        return f"{size:.2f} lots"
    elif market_type == STOCK:
        return f"{size:.4f} shares"
    elif market_type == CRYPTO:
        return f"{size:.6f} coins"
    elif market_type == INDEX:
        return f"{size:.2f} contracts"
    return f"{size}"


def format_pnl(pnl):
    sign = "+" if pnl >= 0 else ""
    return f"{sign}${pnl:.2f}"


def pips_to_price(pips, market_type=FOREX):
    if market_type == FOREX:
        return pips * 0.0001
    return pips