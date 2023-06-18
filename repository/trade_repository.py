import traceback
import os
from flask import jsonify
import mysql.connector
import utils.converters as converters
from dotenv import load_dotenv


if not os.environ.get('IS_HEROKU', None):
    load_dotenv()


conn = mysql.connector.connect(user=os.environ.get("USERNAME"), 
                               password=os.environ.get("PASSWORD"), 
                               host=os.environ.get("HOST"), 
                               database=os.environ.get("DATABASE"))


def get_first_trade(accountID):
    cursor = conn.cursor()
    sql = """
    SELECT MIN(opened) FROM trades_tb
    WHERE accountID=%s
    """
    val = accountID
    cursor.execute(sql, (val,))
    res = cursor.fetchone()
    cursor.close()
    return res[0]


def get_trades(accountID):
    cursor = conn.cursor(dictionary=True)
    sql = """
    SELECT ticketID, accountID, tradeType, symbol, price, sl, tp, swap, profit, closed, opened, outcome
    FROM trades_tb
    WHERE accountID=%s
    """
    val = accountID

    cursor.execute(sql, (val,))
    res = cursor.fetchall()
    cursor.close()
    
    for trade in res:
        trade.update({"opened":str(trade.get("opened"))})
        trade.update({"closed":str(trade.get("closed"))})

    return res



def trade_save(trade):
    cursor = conn.cursor()

    sql = """
    INSERT IGNORE INTO trades_tb
    (ticketID, accountID, tradeType, symbol, size, price, sl, tp, swap, profit, closed, opened, outcome)
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    trade = converters.determine_outcome(trade)
    val = trade.get("ticketID"),trade.get("accountID"),trade.get("type"),trade.get("symbol"),trade.get("size"), trade.get("price"),trade.get("sl"),trade.get("tp"),trade.get("swap"),trade.get("profit"),trade.get("closed"),trade.get("opened"), trade.get("outcome")

    try:
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        return jsonify("New Trade Saved"), 200
    except Exception as e:
        print(traceback.format_exc())
        conn.rollback()
        cursor.close()
        return "Error saving trade", 500


def bulk_save_trades(trades):
    cursor = conn.cursor()

    val_trades = []
    for trade in trades:
        trade = converters.determine_outcome(trade)
        val_trades.append((trade.get("ticketID"),trade.get("accountID"),trade.get("type"),trade.get("symbol"),trade.get("size"), trade.get("price"),trade.get("sl"),trade.get("tp"),trade.get("swap"),trade.get("profit"),trade.get("closed"),trade.get("opened"), trade.get("outcome")))
    sql = """
    INSERT IGNORE INTO trades_tb 
    (ticketID, accountID, tradeType, symbol, size, price, sl, tp, swap, profit, closed, opened, outcome)
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    try: 
        cursor.executemany(sql, val_trades)
        conn.commit()
        cursor.close()
        return jsonify("Bulk trades saved"), 200
    except Exception:
        print(traceback.format_exc())
        conn.rollback()
        cursor.close()
        return "Error bulk saving trades", 500


def save_meta_data(meta_data):
    cursor = conn.cursor()
    
    vals = []

    for val in meta_data:
        vals.append((val.get("ticketID"), val.get("atrVal"), val.get("atrVal5Diff"), val.get("maVal"), val.get("maVal5Diff"), val.get("maValDist"), val.get("rsiVal"), val.get("rsiVal5Diff")))

    sql = """
    INSERT IGNORE INTO meta_data_tb
    (ticketID, atrVal, atrVDiff, maVal, maValDiff, maValDist, rsiVal, rsiValDiff)
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    try:
        cursor.executemany(sql, vals)
        conn.commit()
        cursor.close()
        return jsonify("Meta Data Saved"), 200
    except Exception:
        print(traceback.format_exc())
        conn.rollback()
        cursor.close()
        return "Error Storing Meta Data", 500


def update_result_rows(result_rows):
    cursor = conn.cursor()
    count=0 
    sql = """
        UPDATE meta_data_tb SET result = %s
        WHERE ticketID = %s
    """
    for row in result_rows:
        if outcomeCheck(row.get("result") != "na"):
            try:
                cursor.execute(sql, (outcomeCheck(float(row.get("result"))), row.get("ticketID")))
                conn.commit()
                count+=1
                if (int(row.get("ticketID")) % 100 == 0):
                    print("Successfully Committed Row: "+row.get("ticketID"))
            except Exception:
                print(traceback.format_exc())
                conn.rollback()
                cursor.close()
                return "Error Storing Meta Data", 500
    return "Result Data Saved", 200


def outcomeCheck(res):
    if res > 100:
        return "win"
    elif res < 25:
        return "loss"
    else:
        return "na"

