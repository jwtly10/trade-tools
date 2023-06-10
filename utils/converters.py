def bulk_determine_outcome(trades):
    for trade in trades:
        if (trade.get('swap') + trade.get('profit') > 100):
            trade.update({'outcome':'Win'})
        elif(trade.get('profit') == 0):
            trade.update({'outcome':'NA'})
        elif (trade.get('swap') + trade.get('profit') < -25):
            trade.update({'outcome':'Loss'})
        else:
            trade.update({'outcome':'NA'})
            
    return trades


def determine_outcome(trade):
    if (trade.get('swap') + trade.get('profit') > 100):
        trade.update({'outcome':'Win'})
    elif(trade.get('profit') == 0):
        trade.update({'outcome':'NA'})
    elif (trade.get('swap') + trade.get('profit') < -25):
        trade.update({'outcome':'Loss'})
    else:
        trade.update({'outcome':'NA'})
            
    return trade