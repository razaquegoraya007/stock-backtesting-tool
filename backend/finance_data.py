import yfinance as yf
import pandas as pd

def fetch_data(ticker, start_date, end_date):
    """Fetches historical data for a given ticker within the specified date range."""
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            return None, "No data found for the given ticker and date range."
        data.reset_index(inplace=True)
        return data, None
    except Exception as e:
        return None, f"Failed to fetch data due to: {str(e)}"
