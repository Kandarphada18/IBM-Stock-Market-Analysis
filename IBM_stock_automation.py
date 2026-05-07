import requests
import pandas as pd
import os

API_KEY = "YOUR_API_KEY"

def get_stockprice_info(symbol):
    url = "https://www.alphavantage.co/query"

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": "YOUR_API_KEY"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "Time Series (Daily)" not in data:
        print("API Error or Limit Reached")
        return None

    return data


data = get_stockprice_info("IBM")

if data:

    time_series = data["Time Series (Daily)"]

    new_df = pd.DataFrame.from_dict(time_series, orient="index")

    new_df.rename(columns={
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. volume": "volume"
    }, inplace=True)

    new_df.index.name = "date"

    new_df = new_df.astype(float)

    new_df['daily_change'] = new_df['close'] - new_df['open']
    new_df['ma_5'] = new_df['close'].rolling(5).mean()
    new_df['ma_10'] = new_df['close'].rolling(10).mean()

    csv_file = "IBM_stock_data.csv"

    # IF FILE EXISTS → APPEND + REMOVE DUPLICATES
    if os.path.exists(csv_file):

        old_df = pd.read_csv(csv_file)

        final_df = pd.concat([old_df, new_df.reset_index()])

        final_df.drop_duplicates(subset=["date"], inplace=True)

        final_df.sort_values("date", inplace=True)

    else:
        final_df = new_df.reset_index()

    final_df.to_csv(csv_file, index=False)

    print("✅ Stock data updated successfully!")
    

