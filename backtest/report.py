def print_report(metrics, closed_trades):

    if "error" in metrics:
        print(f"\n{'='*40}")
        print(f"  BACKTEST RESULT: {metrics['error']}")
        print(f"{'='*40}\n")
        return

    print(f"\n{'='*40}")
    print(f"  BACKTEST REPORT")
    print(f"{'='*40}")
    print(f"  Total trades:    {metrics['total_trades']}")
    print(f"  Winners:         {metrics['winners']}")
    print(f"  Losers:          {metrics['losers']}")
    print(f"  Win rate:        {metrics['win_rate']}%")
    print(f"{'='*40}")
    print(f"  Total PnL:       ${metrics['total_pnl']}")
    print(f"  Final balance:   ${metrics['final_balance']}")
    print(f"  Avg win:         ${metrics['avg_win']}")
    print(f"  Avg loss:        ${metrics['avg_loss']}")
    print(f"  Profit factor:   {metrics['profit_factor']}")
    print(f"{'='*40}")
    print(f"  Max drawdown:    {metrics['max_drawdown']}%")
    print(f"  Sharpe ratio:    {metrics['sharpe_ratio']}")
    print(f"{'='*40}\n")

    if closed_trades:
        print("  LAST 5 TRADES:")
        for t in closed_trades[-5:]:
            side = t['side']
            pnl = t['pnl']
            reason = t['reason']
            entry = t['entry_price']
            exit_ = t['exit_price']
            print(f"  {side:5} | entry: {entry:.5f} | exit: {exit_:.5f} | {reason:8} | PnL: ${pnl:.2f}")
        print()