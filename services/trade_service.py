import repository.trade_repository as data

def get_trades_for_account(accountID):
    return data.get_trades(accountID)


def save_trade(trade):
    return data.trade_save(trade)


def bulk_save_trades(trades):
    return data.bulk_save_trades(trades)
