import pandas as pd 

def read_trade_csv_file(inputfile):
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

