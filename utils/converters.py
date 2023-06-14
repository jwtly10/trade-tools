def bulk_determine_outcome(trades):
    for trade in trades:
        if (trade.get('swap') + trade.get('profit') > 100):
            trade.update({'outcome':'win'})
        elif(trade.get('profit') == 0):
            trade.update({'outcome':'NA'})
        elif (trade.get('swap') + trade.get('profit') < -25):
            trade.update({'outcome':'loss'})
        else:
            trade.update({'outcome':'NA'})
            
    return trades


def determine_outcome(trade):
    if (trade.get('swap') + trade.get('profit') > 130):
        trade.update({'outcome':'win'})
    elif(trade.get('profit') == 0):
        trade.update({'outcome':'NA'})
    elif (trade.get('swap') + trade.get('profit') < -25):
        trade.update({'outcome':'loss'})
    else:
        trade.update({'outcome':'NA'})
            
    return trade


def trades_to_dictionary(trades):
    list_trades = []
    dict_trade = {}

    for trade in trades:
        dict_trade.update("")
