import requests
import pandas as pd

API_KEY = "YOUR_API_KEY"

def get_stockprice_info(symbol):
    url = "https://www.alphavantage.co/query"
    
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "Error Message" in data:
        print("API Error:", data["Error Message"])
        return None
    if "Time Series (Daily)" not in data:
        print("API limit or issue:", data)
        return None

    return data


data = get_stockprice_info("IBM")

if data:
    time_series = data["Time Series (Daily)"]

    df = pd.DataFrame.from_dict(time_series, orient="index")

    # Rename properly
    df.rename(columns={
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. volume": "volume"
    }, inplace=True)

    df.index.name = "date"
    df = df.sort_index()

    # Convert to numeric (IMPORTANT)
    df = df.astype(float)

    # ✅ Correct calculations
    df['daily_change'] = df['close'] - df['open']
    df['ma_5'] = df['close'].rolling(5).mean()
    df['ma_10'] = df['close'].rolling(10).mean()

    df.to_csv("IBM_stock_data.csv")

    print("✅ Saved successfully!")
    print(df)