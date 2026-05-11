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

    #DRAWDOWN
    peak = balance_curve[0]
    max_drawdown = 0

    for b in balance_curve:
        if b > peak:
            peak = b
        
        drawdown = (peak - b) / peak * 100
        if drawdown > max_drawdown:
            max_drawdown = drawdown

        # SHARPE RATIO (asume risk-free rate = 0)
        if len(pnls) > 1:
            mean_pnl = np.mean(pnls)
            std_pnl = np.std(pnls)
            sharpe = (mean_pnl / std_pnl) * np.sqrt(252) if std_pnl > 0 else 0
        else:
            sharpe = 0

        return{
            "total_trades": len(pnls),
            "winners": len(winners),
            "losers": len(losers),
            "win_rate": round(win_rate, 2),
            "total_pnl": round(sum(pnls), 2),
            "avg_win": round(np.mean(winners), 2) if winners else 0,
            "avg_loss": round(np.mean(losers), 2) if losers else 0,
            "profit_factor": round(profit_factor, 2),
            "max_drawdown": round(max_drawdown, 2),
            "sharpe_ratio": round(sharpe, 2),
            "final_balance": round(balance_curve[-1], 2)
        }