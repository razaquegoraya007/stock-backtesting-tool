import pandas as pd
from finance_data import fetch_data

def calculate_profit(buy_price, sell_price, amount=1):
    """Calculates the profit or loss from a transaction."""
    return (sell_price - buy_price) * amount

def simple_strategy(data, threshold=0.02):
    """Implements a simple trading strategy based on price increase by a threshold."""
    buy_price = None
    transactions = []

    for index, row in data.iterrows():
        if buy_price is None and row['Close'] > row['Open'] * (1 + threshold):
            buy_price = row['Close']
            buy_date = row['Date']
        elif buy_price and row['Close'] < buy_price * (1 - threshold):
            sell_price = row['Close']
            sell_date = row['Date']
            profit = calculate_profit(buy_price, sell_price)
            transactions.append({
                'buy_date': buy_date,
                'sell_date': sell_date,
                'buy_price': buy_price,
                'sell_price': sell_price,
                'profit': profit
            })
            buy_price = None
    return transactions

def execute_backtest(ticker, start_date, end_date, strategy=simple_strategy, threshold=0.02):
    data, error = fetch_data(ticker, start_date, end_date)
    if error:
        return {"error": error}

    data['Date'] = pd.to_datetime(data['Date'])
    results = strategy(data, threshold)
    if not results:
        return {"error": "No transactions were executed based on the strategy parameters."}
    return results
