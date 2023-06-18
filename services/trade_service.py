import repository.trade_repository as data
import services.csvreader_service as csv
from datetime import datetime

time_format = "%Y-%m-%d %H:%M:%S"

def get_trades_for_account(accountID):
    return data.get_trades(accountID)


def save_trade(trade):
    return data.trade_save(trade)


def meta_data_save_from_csv(file):
    rows = csv.read_meta_data_csv_file(file)
    return data.save_meta_data(rows)

def result_data_save_from_csv(file):
    rows = csv.read_result_data_csv_file(file)
    return data.update_result_rows(rows)


def bulk_save_trades_from_csv(file, accountID):
    trades = csv.read_trade_csv_file(file, accountID) 
    return data.bulk_save_trades(trades)


def bulk_save_trades(trades):
    return data.bulk_save_trades(trades)


def get_first_trade(accountID):
    return data.get_first_trade(accountID)


def get_days_since_first_trade(date):
    today = datetime.utcnow()
    delta = today - date
    return delta.days
