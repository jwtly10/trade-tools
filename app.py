from flask import Flask, jsonify, request
import os
import mysql.connector
from dotenv import load_dotenv
import services.data_queries as data
import services.statistics as stats
if not os.environ.get('IS_HEROKU', None):
    load_dotenv()

conn = mysql.connector.connect(user=os.environ.get("USERNAME"), password=os.environ.get("PASSWORD"), host=os.environ.get("HOST"), database=os.environ.get("DATABASE"))

app = Flask(__name__)

@app.route("/gettradestats")
def get_trade_stats():
    stats_json = {}
    accountID = request.args.get('accountID')
    trade_type = request.args.get('type')
    trades = data.get_trades(accountID, conn)
    stats_json.update({"average_open_time": stats.get_average_trade_time(trades, trade_type.lower())})
 

    return jsonify(stats_json)



@app.route("/gettrades")
def get_trades():
    accountID = request.args.get('accountID')
    if accountID:
        trades = data.get_trades(accountID, conn) 
        if len(trades)==0:
            return f"No trades found for Account {accountID}", 400
        else:
            return jsonify(data.get_trades(accountID, conn)), 200
    else:
        return 'Account id is missing', 400


@app.route('/newtrade', methods=['POST'])
def add_new_trade():
    trade = request.get_json()
    data.trade_save(trade, conn)

    return 'New Trade Saved', 200


@app.route('/bulktrades', methods=['POST'])
def bulk_upload_trades():
    trades = request.get_json()
    data.bulk_save_trades(trades, conn)

    return 'Bulk Trades Upload', 200


if __name__ == '__main__':
    app.run()