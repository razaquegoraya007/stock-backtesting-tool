from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
from backtesting_engine import strategy_with_mql4_logic

app = Flask(__name__)
CORS(app)

@app.route('/backtest', methods=['GET'])
def backtest():
    ticker = request.args.get('ticker')
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    percent_change = float(request.args.get('percent_change', 1.0))
    positive_change = request.args.get('positive_change', 'true').lower() == 'true'
    trade_direction = int(request.args.get('trade_direction', 1))
    max_trades_per_day = int(request.args.get('max_trades_per_day', 1))
    use_take_profit_minutes = request.args.get('use_take_profit_minutes', 'true').lower() == 'true'
    take_profit_minutes = int(request.args.get('take_profit_minutes', 60))
    use_take_profit_daily_close = request.args.get('use_take_profit_daily_close', 'true').lower() == 'true'
    use_stop_loss = request.args.get('use_stop_loss', 'false').lower() == 'true'
    stop_loss_points = int(request.args.get('stop_loss_points', 100))
    entry_mode = int(request.args.get('entry_mode', 0))
    use_start_time = request.args.get('use_start_time', 'false').lower() == 'true'
    start_hour = int(request.args.get('start_hour', 0))
    start_minute = int(request.args.get('start_minute', 0))
    daily_close_hour = int(request.args.get('daily_close_hour', 23))
    daily_close_minute = int(request.args.get('daily_close_minute', 59))

    if not all([ticker, start_date, end_date]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        # Fetch data from Yahoo Finance using yfinance
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        stock_data.reset_index(inplace=True)

        # Run the backtesting strategy
        results = strategy_with_mql4_logic(
            stock_data,
            percent_change=percent_change,
            positive_change=positive_change,
            trade_direction=trade_direction,
            max_trades_per_day=max_trades_per_day,
            use_take_profit_minutes=use_take_profit_minutes,
            take_profit_minutes=take_profit_minutes,
            use_take_profit_daily_close=use_take_profit_daily_close,
            use_stop_loss=use_stop_loss,
            stop_loss_points=stop_loss_points,
            entry_mode=entry_mode,
            use_start_time=use_start_time,
            start_hour=start_hour,
            start_minute=start_minute,
            daily_close_hour=daily_close_hour,
            daily_close_minute=daily_close_minute
        )

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
