import numpy as np

def calculate_metrics(closed_trades, initial_balance):
    if not closed_trades:
        return {"error": "No closed trades"}
    
    pnls = [t['pnl'] for t in closed_trades]
    balance_curve = [initial_balance]

    for pnl in pnls:
        balance_curve.append(balance_curve[-1] + pnl)

    winners = [p for p in pnls if p > 0]
    losers = [p for p in pnls if p <= 0]

    win_rate = len(winners) / len(pnls) * 100

    profit_factor = (
        sum(winners) / abs(sum(losers))
        if losers else float('inf')
    )

    # DRAWDOWN
    peak = balance_curve[0]
    max_drawdown = 0
    for b in balance_curve:
        if b > peak:
            peak = b
        drawdown = (peak - b) / peak * 100
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    #SHARPE
    if len(pnls) > 1:
        mean_pnl = np.mean(pnls)
        std_pnl = np.std(pnls)
        sharpe = (mean_pnl / std_pnl) * np.sqrt(252) if std_pnl > 0 else 0
    else:
        sharpe = 0

    # EXPECTANCY - cuanto ganas en promedio por trade arriesgando $1
    avg_win = np.mean(winners) if winners else 0
    avg_loss = abs(np.mean(losers)) if losers else 0
    expectancy = (win_rate / 100 * avg_win) - ((1 - win_rate / 100) * avg_loss)

    #RISK/REWARD PROMEDIO
    rr_ratio = avg_win / avg_loss if avg_loss > 0 else 0

    # MAX CONSECUTIVE LOSSES
    max_consec_losses = 0
    current_consec = 0
    for p in pnls:
        if p <= 0:
            current_consec += 1
            max_consec_losses = max(max_consec_losses, current_consec)
        else:
            current_consec = 0

    # MAX CONSECUTIVE WINS
    max_consec_wins = 0
    current_consec = 0
    for p in pnls:
        if p > 0:
            current_consec += 1
            max_consec_wins = max(max_consec_wins, current_consec)
        else:
            current_consec = 0

    return {
        "total_trades":       len(pnls),
        "winners":            len(winners),
        "losers":             len(losers),
        "win_rate":           round(win_rate, 2),
        "total_pnl":          round(sum(pnls), 2),
        "avg_win":            round(avg_win, 2),
        "avg_loss":           round(-avg_loss, 2),
        "profit_factor":      round(profit_factor, 2),
        "expectancy":         round(expectancy, 2),
        "rr_ratio":           round(rr_ratio, 2),
        "max_drawdown":       round(max_drawdown, 2),
        "sharpe_ratio":       round(sharpe, 2),
        "max_consec_losses":  max_consec_losses,
        "max_consec_wins":    max_consec_wins,
        "final_balance":      round(balance_curve[-1], 2)
    }