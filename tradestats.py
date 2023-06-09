from datetime import datetime as dt
import pandas as pd 
import performance

def main():
    # trades = readTradeCSVFile('initial_load.csv')

    # Local list of trades for testing performance
    # instead of reading from file every time
    trades = performance.tradeJSON
    # print(trades)

    trades = determinoutcome(trades)
    avgtradetime = getavgtradetime(trades, True)
    print(avgtradetime)
    avgtradetime = getavgtradetime(trades, False)
    print(avgtradetime)


def determinoutcome(trades):
    for trade in trades:
        if (trade.get('swap') + trade.get('profit') > 100):
            trade.update({'win':'True'})
        elif (trade.get('swap') + trade.get('profit') < -25):
            trade.update({'win':'False'})
        else:
            trade.update({'win':'NA'})
            
    return trades


def getavgtradetime(trades, winning_trade):
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


def readTradeCSVFile(inputfile):
    trades = []
    trade = {}

    my_converter = {'accountID': str, 'ticketID': str}
    df = pd.read_csv(inputfile, converters=my_converter)
    
    for row in range(len(df.index)):
        try:
           # Put everything in a list of dictionaries
           trade.update({'ticketID':str(df.iloc[row]['ticketID'])})
           trade.update({'accountID':str(df.iloc[row]['accountID'])})
           trade.update({'type':df.iloc[row]['type']})
           trade.update({'size':df.iloc[row]['size']})
           trade.update({'symbol':df.iloc[row]['symbol']})
           trade.update({'price':df.iloc[row]['price']})
           trade.update({'sl':df.iloc[row]['sl']})
           trade.update({'tp':df.iloc[row]['tp']})
           trade.update({'swap':df.iloc[row]['swap']})
           trade.update({'profit':df.iloc[row]['profit']})
           trade.update({'closed':df.iloc[row]['closed']})
           trade.update({'created':df.iloc[row]['created']})
               
           trades.append(trade.copy())
        except Exception as e:
            print(f'Error: {e}')
    
    return trades


if __name__ == "__main__":
    main()