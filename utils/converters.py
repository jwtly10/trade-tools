def determine_outcome(trades):
    for trade in trades:
        if (trade.get('swap') + trade.get('profit') > 100):
            trade.update({'win':'True'})
        elif (trade.get('swap') + trade.get('profit') < -25):
            trade.update({'win':'False'})
        else:
            trade.update({'win':'NA'})
            
    return trades