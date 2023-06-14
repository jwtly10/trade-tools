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

    stats_json.update({"average_return_per_trade_all":
                      average_return_per_trade_all(trades)})

    stats_json.update({"all_time_pnl":
                      all_time_pnl(trades)})

    trade_type_numbers = get_number_of_trade_types(trades)
    stats_json.update({"number_of_losses":
                      trade_type_numbers[1]})

    stats_json.update({"number_wins":
                      trade_type_numbers[0]})

    stats_json.update({"number_nas":
                      trade_type_numbers[2]})
 

    return stats_json


def get_number_of_trade_types(trades):
    wins=0
    losses=0
    nas=0
    for trade in trades:
        if trade.get('outcome') == "win":
            wins+=1
        elif trade.get('outcome') == "loss":
            losses+=1
        else:
            nas+=1
    return wins, losses, nas


def average_return_per_trade_all(trades):
    total = 0
    for trade in trades:
        total = total + trade.get("swap") + trade.get("profit")

    return round(total / len(trades), 2)

def all_time_pnl(trades):
    pnl=0
    for trade in trades:
        pnl = pnl + trade.get("swap") + trade.get("profit")
    
    return pnl

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
    ntrades=0
    diff=0
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
