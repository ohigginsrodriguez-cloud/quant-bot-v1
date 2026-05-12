def print_report(metrics, closed_trades):

    if "error" in metrics:
        print(f"\n{'='*40}")
        print(f"  BACKTEST RESULT: {metrics['error']}")
        print(f"{'='*40}\n")
        return

    print(f"\n{'='*40}")
    print(f"  BACKTEST REPORT")
    print(f"{'='*40}")
    print(f"  Total trades:        {metrics['total_trades']}")
    print(f"  Winners:             {metrics['winners']}")
    print(f"  Losers:              {metrics['losers']}")
    print(f"  Win rate:            {metrics['win_rate']}%")
    print(f"  Max consec. wins:    {metrics['max_consec_wins']}")
    print(f"  Max consec. losses:  {metrics['max_consec_losses']}")
    print(f"{'='*40}")
    print(f"  Total PnL:           ${metrics['total_pnl']}")
    print(f"  Final balance:       ${metrics['final_balance']}")
    print(f"  Avg win:             ${metrics['avg_win']}")
    print(f"  Avg loss:            ${metrics['avg_loss']}")
    print(f"  Profit factor:       {metrics['profit_factor']}")
    print(f"  Expectancy:          ${metrics['expectancy']} per trade")
    print(f"  Risk/Reward avg:     {metrics['rr_ratio']}")
    print(f"{'='*40}")
    print(f"  Max drawdown:        {metrics['max_drawdown']}%")
    print(f"  Sharpe ratio:        {metrics['sharpe_ratio']}")
    print(f"{'='*40}\n")

    if closed_trades:
        print("  LAST 5 TRADES:")
        for t in closed_trades[-5:]:
            print(f"  {t['side']:5} | entry: {t['entry_price']:.5f} | exit: {t['exit_price']:.5f} | {t['reason']:8} | PnL: ${t['pnl']:.2f}")
        print()