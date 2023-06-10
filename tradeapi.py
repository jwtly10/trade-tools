from flask import Flask, jsonify, request
import mysql.connector
import server_settings_dev as dev
import traceback

conn = mysql.connector.connect(user=dev.username, password=dev.password, host=dev.endpoint, database=dev.database)

app = Flask(__name__)

# @app.route("/")
# def show_trades():
#     return jsonify(trades)

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

def trade_save(trade):
    cursor = conn.cursor()

    sql = """
    INSERT INTO trades_tb 
    (ticketID, accountID, tradeType, symbol, price, sl, tp, swap, profit, closed, opened, outcome)
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    
    ticketID = trade.get("ticketID")
    accountID = trade.get("accountID")
    tradeType = trade.get("type")
    symbol = trade.get("symbol")
    price = trade.get("price")
    sl = trade.get("sl")
    tp = trade.get("tp")
    swap = trade.get("swap")
    profit = trade.get("profit")
    closed = trade.get("closed")
    created = trade.get("created")
    outcome = trade.get("outcome")
    
    val = ticketID, accountID, tradeType, symbol, price, sl, tp, swap, profit, closed, created, outcome 
    
    try:
        cursor.execute(sql, val)
        conn.commit()
    except Exception:
        print(traceback.format_exc())
        conn.rollback()

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
    except Exception:
        print(traceback.format_exc())
        conn.rollback()
