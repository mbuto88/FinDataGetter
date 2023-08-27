import yfinance as yf
import pandas as pd
import os

import pandas as pd


def fetch_data(symbols):
    for symbol in symbols:
        print(f"Getting stock data for {symbol}")
        filename = f'{symbol}_5_year_history.csv'
        filepath = f'./historical-data/{filename}'

        # Define the 5-year period
        start_date = pd.to_datetime('today') - pd.DateOffset(years=5)
        end_date = pd.to_datetime('today')

        # Fetch the new stock data
        new_stock_data = fetch_stock_data(symbol, start_date, end_date)

        # Check if the CSV file already exists
        try:
            existing_stock_data = pd.read_csv(filepath, parse_dates=['Date'])
        except FileNotFoundError:
            existing_stock_data = pd.DataFrame()

        # If the file exists, concatenate and remove duplicates
        if not existing_stock_data.empty:
            combined_stock_data = pd.concat([existing_stock_data, new_stock_data])
            combined_stock_data.drop_duplicates(subset=['Date'], keep='last', inplace=True)
            combined_stock_data.sort_values(by='Date', inplace=True)
        else:
            combined_stock_data = new_stock_data

        # Write the combined data back to the CSV
        write_to_csv(combined_stock_data, filename)
        print(f"{symbol} 5-year history has been updated in historical-data/{filename}")


def fetch_stock_data(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    data = yf.download(stock, start=start_date, end=end_date)
    return data



def write_to_csv(data, filename):
    folder_name = 'historical-data'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    full_path = os.path.join(folder_name, filename)

    if os.path.exists(full_path):
        existing_data = pd.read_csv(full_path)
        data = pd.concat([existing_data, data]).drop_duplicates(subset='Date').sort_values('Date')

    data.to_csv(full_path, index=False)
