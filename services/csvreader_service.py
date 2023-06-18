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


def read_meta_data_csv_file(inputfile):
    meta_rows = []
    data = {}

    my_converter = {'ticketID': str}
    df = pd.read_csv(inputfile, converters=my_converter)
    
    for row in range(len(df.index)):
        try:
           # Put everything in a list of dictionaries
           data.update({'ticketID':str(df.iloc[row]['ticketID'])})
           data.update({'atrVal':str(df.iloc[row]['atrVal'])})
           data.update({'atrVal5Diff':str(df.iloc[row]['atrVal5Diff'])})
           data.update({'maVal':str(df.iloc[row]['maVal'])})
           data.update({'maVal5Diff':str(df.iloc[row]['maVal5Diff'])})
           data.update({'maValDist':str(df.iloc[row]['maValDist'])})
           data.update({'rsiVal':str(df.iloc[row]['rsiVal'])})
           data.update({'rsiVal5Diff':str(df.iloc[row]['rsiVal5Diff'])})
               
           meta_rows.append(data.copy())
        except Exception as e:
            print(f'Error: {e}')
    
    return meta_rows


def read_result_data_csv_file(inputfile):
    result_rows = []
    data = {}

    my_converter = {'ticketid': str}
    df = pd.read_csv(inputfile, converters=my_converter)
    
    for row in range(len(df.index)):
        try:
           # Put everything in a list of dictionaries
           data.update({'ticketID':str(df.iloc[row]['ticketid'])})
           data.update({'result':str(df.iloc[row]['result'])})
               
           result_rows.append(data.copy())
        except Exception as e:
            print(f'Error: {e}')
    
    return result_rows
