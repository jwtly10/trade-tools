from datetime import datetime as dt

def get_average_trade_time(trades, trade_type):
    time_format = "%Y-%m-%d %H:%M:%S"
    diff=0
    ntrades=0
    if trade_type: 
        print("Averaging winning trades")
    else:
        print("Averaging losing trades")

    for trade in trades:
        t1 = dt.strptime(trade.get('opened'), time_format)
        t2 = dt.strptime(trade.get('closed'), time_format)
        delta = t2-t1

        if trade_type:
            if trade.get('outcome') == "win": # Average outcomening trades
                ntrades+=1
                print(f"Opened  : {trade.get('opened')} Closed: {trade.get('closed')} - Diff: {delta.total_seconds()} - Profit: {trade.get('profit')}")
                diff = diff + delta.total_seconds()
        else:
            if trade.get('outcome') == "loss": # Average losing trades
                ntrades+=1
                print(f"Opened: {trade.get('opened')} Closed: {trade.get('closed')} - Diff: {delta.total_seconds()} - Profit: {trade.get('profit')}")
                diff = diff + delta.total_seconds()

    print(f"Number of Trades: {ntrades:}") 
    return round(diff / ntrades)