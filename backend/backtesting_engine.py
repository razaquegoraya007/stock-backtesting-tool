import pandas as pd
from datetime import timedelta

def strategy_with_mql4_logic(data, percent_change=1.0, positive_change=True,
                             trade_direction=1, max_trades_per_day=1,
                             use_take_profit_minutes=True, take_profit_minutes=60,
                             use_take_profit_daily_close=True, use_stop_loss=False,
                             stop_loss_points=100, entry_mode=0,
                             use_start_time=False, start_hour=0, start_minute=0,
                             daily_close_hour=23, daily_close_minute=59):
    """Implements the strategy logic based on the MQL4 strategy."""

    # Initialize variables
    buy_price = None
    open_time = None
    open_price = None
    trades_today = 0
    last_trade_day = None
    transactions = []

    # Loop through the data for each tick (row in the DataFrame)
    for index, row in data.iterrows():
        current_day = row['Date'].date()

        # Reset trades if day changes
        if last_trade_day != current_day:
            trades_today = 0
            last_trade_day = current_day

        # Custom start time logic
        if use_start_time:
            start_time = pd.Timestamp(current_day) + timedelta(hours=start_hour, minutes=start_minute)
        else:
            start_time = pd.Timestamp(current_day)

        # Calculate reference price based on entry mode
        if entry_mode == 0:
            reference_price = data.iloc[index - 1]['Close'] if index > 0 else row['Open']
        else:
            reference_price = row['Open']

        # Adjust reference price if using a specific start time
        if use_start_time and pd.Timestamp(row['Date']) >= start_time:
            reference_price = row['Close']

        # Calculate percentage change
        current_price = row['Close']
        percent_move = ((current_price - reference_price) / reference_price) * 100

        # Determine if we should open a trade based on the percentage change
        change_condition_met = (positive_change and percent_move >= percent_change) or \
                               (not positive_change and percent_move <= -percent_change)

        # Open trade logic if conditions are met
        if trades_today < max_trades_per_day and open_time is None and open_price is None and change_condition_met:
            # Set Stop Loss
            sl_price = None
            if use_stop_loss:
                if trade_direction == 1:  # Buy
                    sl_price = current_price - stop_loss_points
                elif trade_direction == -1:  # Sell
                    sl_price = current_price + stop_loss_points

            # Open Buy/Sell trade based on trade direction
            if trade_direction == 1:  # Buy
                buy_price = current_price
                open_time = row['Date']
                open_price = buy_price
            elif trade_direction == -1:  # Sell
                open_price = current_price
                open_time = row['Date']

            trades_today += 1  # Increment the trade count for the day

        # Take Profit Logic (in minutes)
        if use_take_profit_minutes and open_time is not None:
            minutes_passed = (row['Date'] - open_time).total_seconds() / 60
            if minutes_passed >= take_profit_minutes:
                transactions.append({
                    'buy_date': open_time,
                    'sell_date': row['Date'],
                    'buy_price': buy_price if trade_direction == 1 else None,
                    'sell_price': current_price if trade_direction == 1 else None,  # Set sell price for the buy
                    'profit': (current_price - open_price) if trade_direction == 1 else (open_price - current_price)
                })
                open_time = None
                open_price = None

        # Take Profit at Daily Close
        daily_close_time = pd.Timestamp(current_day) + timedelta(hours=daily_close_hour, minutes=daily_close_minute)
        if use_take_profit_daily_close and open_time is not None:
            if pd.Timestamp(row['Date']) >= daily_close_time:
                transactions.append({
                    'buy_date': open_time,
                    'sell_date': row['Date'],
                    'buy_price': buy_price if trade_direction == 1 else None,
                    'sell_price': current_price if trade_direction == -1 else None,  # Set sell price for the sell
                    'profit': (current_price - open_price) if trade_direction == 1 else (open_price - current_price)
                })
                open_time = None
                open_price = None

    return transactions
