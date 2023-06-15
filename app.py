from flask import Flask, jsonify, make_response, request
import json
import logging
import os
from os.path import join, dirname, realpath
from numpy import who
import services.trade_service as trade
import services.stats_service as stats
import utils.crypto as crypto

app = Flask(__name__)
logging.basicConfig(level = logging.INFO)

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/gettradestats")
def get_trade_stats():
    stats_json = {}
    accountID = request.args.get('accountID')
    stats_json = stats.build_statistics(accountID)

    response = make_response(jsonify(stats_json))
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response,  200


@app.route("/gettrades")
def get_trades():
    trades=[]
    accountID = request.args.get('accountID')
    if accountID:
        trades = trade.get_trades_for_account(accountID) 
        if not trades: 
            return f"No trades found for Account {accountID}", 400
        else:
            response = make_response(jsonify(trades))
            response.headers.add('Access-Control-Allow-Origin', '*')

            return response, 200
    else:
        return 'Account id is missing', 400


@app.route('/newtrade', methods=['POST'])
def add_new_trade():
    trade_data = request.get_json()
    if request.headers.get("HMAC_TRADE_DATA"):
        if crypto.verify_request(os.environ.get("X-API-KEY"), json.dumps(trade_data).replace(": ", ":").replace(", ", ","), request.headers.get("HMAC_TRADE_DATA").upper()):
            return trade.save_trade(trade_data)
        else:
            return make_response(jsonify("Verification Failed")), 401
    else:
        return make_response(jsonify("Verification Header missing")), 401


@app.route('/bulktrades', methods=['POST'])
def bulk_upload_trades():
    trade_data = request.get_json()
    if request.headers.get("HMAC_TRADE_DATA"):
        if crypto.verify_request(os.environ.get("X-API-KEY"), json.dumps(trade_data).replace(": ", ":").replace(", ", ","), request.headers.get("HMAC_TRADE_DATA").upper()):
            return trade.bulk_save_trades(trade_data)
        else:
            return make_response(jsonify("Verification Failed")), 401
    else:
        return make_response(jsonify("Verification Header missing")), 401


@app.route('/csvbulktrades', methods=['POST'])
def upload_file():
    accountID  = request.args.get("accountID")
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
    
    return trade.bulk_save_trades_from_csv(file_path, accountID)


@app.after_request
def log_response(response):
    logging.info(f"RESPONSE data = {response.get_data()}")
    return response


@app.before_request
def log_request():
    logging.info(f"NEW REQUEST method = {request.method} user-agent = {request.headers.get('User-Agent')} content-length = {request.headers.get('Content-Length')}")
    pass


if __name__ == '__main__':
    app.run
