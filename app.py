from flask import Flask, jsonify, request
import mysql.connector
import server_settings_dev as dev
import traceback

conn = mysql.connector.connect(user=dev.username, password=dev.password, host=dev.endpoint, database=dev.database)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return "Trade Tools Running."

@app.route("/")
def get_trade():
    accountID = request.args.get('accountID')

    return jsonify(get_trades(accountID)), 200


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