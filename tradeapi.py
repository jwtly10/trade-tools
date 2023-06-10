from flask import Flask, jsonify, request


trades = []

app = Flask(__name__)

@app.route("/")
def show_trades():
    return jsonify(trades)

@app.route('/newtrade', methods=['POST'])
def add_new_trade():
    trades.append(request.get_json())
    return 'New Trade Saved', 200

@app.route('/bulktrades', methods=['POST'])
def bulk_upload_trades():
    trades.append(request.get_json())

    for trade in trades[0]:
        print(trade)
        print()

    return 'Bulk Trades Upload', 200
