from flask import Flask, jsonify, request
import services.trade_service as trade
import services.stats_service as stats

app = Flask(__name__)

@app.route("/gettradestats")
def get_trade_stats():
    stats_json = {}
    accountID = request.args.get('accountID')
    stats_json = stats.build_statistics(accountID)


    return jsonify(stats_json), 200


@app.route("/gettrades")
def get_trades():
    trades=[]
    accountID = request.args.get('accountID')
    if accountID:
        trades = trade.get_trades_for_account(accountID) 
        if not trades: 
            return f"No trades found for Account {accountID}", 400
        else:
            return jsonify(trades), 200
    else:
        return 'Account id is missing', 400


@app.route('/newtrade', methods=['POST'])
def add_new_trade():
    trade_data = request.get_json()
    return trade.save_trade(trade_data)


@app.route('/bulktrades', methods=['POST'])
def bulk_upload_trades():
    trades = request.get_json()
    return trade.bulk_save_trades(trades)


if __name__ == '__main__':
    app.run()
