from datetime import datetime as dt

def get_average_trade_time(trades, winning_trade):
    time_format = "%Y.%m.%d %H:%M:%S"
    diff=0
    ntrades=0
    if winning_trade: 
        print("Averaging winning trades")
    else:
        print("Averaging losing trades")

    for trade in trades:
        t1 = dt.strptime(trade.get('created'), time_format)
        t2 = dt.strptime(trade.get('closed'), time_format)
        delta = t2-t1

        if winning_trade:
            if trade.get('win') == "True": # Average winning trades
                ntrades+=1
                print(f"Created: {trade.get('created')} Closed: {trade.get('closed')} - Diff: {delta.total_seconds()} - Profit: {trade.get('profit')}")
                diff = diff + delta.total_seconds()
        else:
            if trade.get('win') == "False": # Average losing trades
                ntrades+=1
                print(f"Created: {trade.get('created')} Closed: {trade.get('closed')} - Diff: {delta.total_seconds()} - Profit: {trade.get('profit')}")
                diff = diff + delta.total_seconds()

    print(f"Number of Trades: {ntrades:}") 
    return diff / ntrades