from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

@app.route('/backtest', methods=['GET'])
def backtest():
    ticker = request.args.get('ticker')
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    if not all([ticker, start_date, end_date]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        # Fetch data from Yahoo Finance using yfinance
        stock_data = yf.download(ticker, start=start_date, end=end_date)

        # Prepare results in the required format
        results = []
        for index, row in stock_data.iterrows():
            results.append({
                "date": index.strftime('%Y-%m-%d'),  # Format the date
                "open": row['Open'],
                "high": row['High'],
                "low": row['Low'],
                "close": row['Close'],
                "volume": row['Volume'],
                "ticker": ticker,
                "trades_in_gain": 5,  # Example static value, replace with actual logic
                "total_gain": "10%",  # Example static value, replace with actual logic
                "percentage_gain": "10%",  # Example static value, replace with actual logic
                "trades_in_loss": 2,  # Example static value, replace with actual logic
                "total_loss": "5%",  # Example static value, replace with actual logic
                "percentage_loss": "5%",  # Example static value, replace with actual logic
                "total_trades": 7,  # Example static value, replace with actual logic
                "result_percentage": "5%",  # Example static value, replace with actual logic
                "max_drawdown_percentage": "-3%",  # Example static value, replace with actual logic
                "max_gain_per_trade_percentage": "4%",  # Example static value, replace with actual logic
                "medium_gain": "2%",  # Example static value, replace with actual logic
                "medium_volume": "100000"  # Example static value, replace with actual logic
            })

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
