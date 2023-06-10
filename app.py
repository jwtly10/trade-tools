from flask import Flask, jsonify, request
import os
import mysql.connector
import traceback
from dotenv import load_dotenv

if not os.environ.get('IS_HEROKU', None):
    load_dotenv()

conn = mysql.connector.connect(user=os.environ.get("USERNAME"), password=os.environ.get("PASSWORD"), host=os.environ.get("HOST"), database=os.environ.get("DATABASE"))

app = Flask(__name__)


@app.route("/")
def get_trade():
    accountID = request.args.get('accountID')
    if accountID:
        return jsonify(get_trades(accountID)), 200
    else:
        return 'Trade-tools-api'


@app.route('/newtrade', methods=['POST'])
def add_new_trade():
    trade = request.get_json()
    trade_save(trade)

    return 'New Trade Saved', 200


@app.route('/bulktrades', methods=['POST'])
def bulk_upload_trades():
    trades = request.get_json()
    bulk_save_trades(trades)

    return 'Bulk Trades Upload', 200


def get_trades(accountID):
    cursor = conn.cursor()
    sql = """
    SELECT ticketID, accountID, tradeType, symbol, price, sl, tp, swap, profit, closed, opened, outcome
    FROM trades_tb
    WHERE accountID=%s
    """
    val = accountID

    cursor.execute(sql, (val,))
    res = cursor.fetchall()
    cursor.close()
    return res


def trade_save(trade):
    cursor = conn.cursor()

    sql = """
    INSERT INTO trades_tb 
    (ticketID, accountID, tradeType, symbol, price, sl, tp, swap, profit, closed, opened, outcome)
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    val = trade.get("ticketID"),trade.get("accountID"),trade.get("type"),trade.get("symbol"),trade.get("price"),trade.get("sl"),trade.get("tp"),trade.get("swap"),trade.get("profit"),trade.get("closed"),trade.get("created"), trade.get("outcome")

    try:
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
    except Exception:
        print(traceback.format_exc())
        conn.rollback()
        cursor.close()

def bulk_save_trades(trades):
    cursor = conn.cursor()

    val_trades = []
    for trade in trades:
         val_trades.append((trade.get("ticketID"),trade.get("accountID"),trade.get("type"),trade.get("symbol"),trade.get("price"),trade.get("sl"),trade.get("tp"),trade.get("swap"),trade.get("profit"),trade.get("closed"),trade.get("created"), trade.get("outcome")))

    sql = """
    INSERT INTO trades_tb 
    (ticketID, accountID, tradeType, symbol, price, sl, tp, swap, profit, closed, opened, outcome)
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    try: 
        cursor.executemany(sql, val_trades)
        conn.commit()
        cursor.close()
    except Exception:
        print(traceback.format_exc())
        conn.rollback()
        cursor.close()


if __name__ == '__main__':
    app.run()