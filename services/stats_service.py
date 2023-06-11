from datetime import datetime as dt
import services.trade_service as trade
time_format = "%Y-%m-%d %H:%M:%S"

def build_statistics(accountID):
    stats_json = {}
    trades = []
    trades = trade.get_trades_for_account(accountID)

    stats_json.update({"average_loss_open_time":
                       get_average_trade_time(trades,'loss')})

    stats_json.update({"average_win_open_time":
                       get_average_trade_time(trades,'win')})

    stats_json.update({"todays_pnl": 
                       get_todays_pnl(trades)})

    stats_json.update({"first_trade":
                       get_first_trade(accountID)})

    stats_json.update({"days_since_first_trade":
                       get_days_since_first_trade(stats_json.get("first_trade"))})

    return stats_json


def get_todays_pnl(trades):
    pnl=0

    for trade in trades:
        if dt.strptime(trade.get("closed"), time_format).date() == dt.today().date():
            pnl = pnl + trade.get("swap") + trade.get("profit")
           
    return pnl


def get_first_trade(accountID):
    return trade.get_first_trade(accountID)

def get_days_since_first_trade(date):
    return trade.get_days_since_first_trade(date)



def get_average_trade_time(trades, trade_type):
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

        if trade_type=='win':
            if trade.get('outcome') == "win": # Average winning trades
                ntrades+=1
                diff = diff + delta.total_seconds()
        else:
            if trade.get('outcome') == "loss": # Average losing trades
                ntrades+=1
                diff = diff + delta.total_seconds()

    print(f"Number of Trades: {ntrades:}") 
    return round(diff / ntrades)
