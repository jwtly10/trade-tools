import traceback
from datetime import datetime
import utils.converters as converters

def get_trades(accountID, conn):
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


def trade_save(trade, conn):
    cursor = conn.cursor()

    sql = """
    INSERT INTO trades_tb 
    (ticketID, accountID, tradeType, symbol, price, sl, tp, swap, profit, closed, opened, outcome)
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    trade = converters.determine_outcome(trade)
    val = trade.get("ticketID"),trade.get("accountID"),trade.get("type"),trade.get("symbol"),trade.get("price"),trade.get("sl"),trade.get("tp"),trade.get("swap"),trade.get("profit"),trade.get("closed"),trade.get("opened"), trade.get("outcome")

    try:
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
    except Exception:
        print(traceback.format_exc())
        conn.rollback()
        cursor.close()


def bulk_save_trades(trades, conn):
    cursor = conn.cursor()

    val_trades = []
    for trade in trades:
        trade = converters.determine_outcome(trade)
        val_trades.append((trade.get("ticketID"),trade.get("accountID"),trade.get("type"),trade.get("symbol"),trade.get("price"),trade.get("sl"),trade.get("tp"),trade.get("swap"),trade.get("profit"),trade.get("closed"),trade.get("opened"), trade.get("outcome")))

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