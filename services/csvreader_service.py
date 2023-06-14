import pandas as pd 

def read_trade_csv_file(inputfile, accountID):
    trades = []
    trade = {}

    my_converter = {'accountID': str, 'ticketID': str}
    df = pd.read_csv(inputfile, converters=my_converter)
    
    for row in range(len(df.index)):
        try:
           # Put everything in a list of dictionaries
           trade.update({'ticketID':str(df.iloc[row]['ticket'])})
           trade.update({'accountID':accountID})
           trade.update({'type':df.iloc[row]['type']})
           trade.update({'size':float(df.iloc[row]['size'])})
           trade.update({'symbol':df.iloc[row]['item']})
           trade.update({'price':float(df.iloc[row]['price'])})
           trade.update({'sl':float(df.iloc[row]['sl'])})
           trade.update({'tp':float(df.iloc[row]['tp'])})
           trade.update({'swap':float(df.iloc[row]['swap'])})
           trade.update({'profit':float(df.iloc[row]['profit'])})
           trade.update({'closed':df.iloc[row]['closed']})
           trade.update({'opened':df.iloc[row]['opened']})
               
           trades.append(trade.copy())
        except Exception as e:
            print(f'Error: {e}')
    
    return trades

