import traceback

def get_trades(accountID, conn):
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


def trade_save(trade, conn):
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

def bulk_save_trades(trades, conn):
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