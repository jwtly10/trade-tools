from flask import Flask, jsonify, request
import os
import mysql.connector
import services.data_queries as data
from dotenv import load_dotenv

if not os.environ.get('IS_HEROKU', None):
    load_dotenv()

conn = mysql.connector.connect(user=os.environ.get("USERNAME"), password=os.environ.get("PASSWORD"), host=os.environ.get("HOST"), database=os.environ.get("DATABASE"))

app = Flask(__name__)


@app.route("/")
def get_trade():
    accountID = request.args.get('accountID')
    if accountID:
        return jsonify(data.get_trades(accountID, conn)), 200
    else:
        return 'Trade-tools-api'


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