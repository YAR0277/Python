import yfinance as yf
import pandas as pd
import time
from pathlib import Path
from datetime import datetime, timedelta

# Compute yesterday's date range
today = datetime.now().date()
yesterday = today - timedelta(days=1)

# Skip weekends
if yesterday.weekday() == 5:  # Saturday
    yesterday -= timedelta(days=1)
elif yesterday.weekday() == 6:  # Sunday
    yesterday -= timedelta(days=2)

start = datetime.combine(yesterday, datetime.min.time())
end = start + timedelta(days=1)

# script directory ... Project/Python
base_path = Path(__file__).resolve().parent

# ETF.txt file path
tickers_file_path = base_path.parent / "Batch" / "Intraday.txt"

# ingest tickers from file
with open(tickers_file_path, "r") as file:
    tickers = [line.strip() for line in file if line.strip()]

# download tickers to data folder
data_folder = base_path.parent.parent / "data" / "finance" / "intraday"
for ticker in tickers:
    data = yf.download(ticker,start=start,end=end,interval="1m",progress=False)

    data = data.tz_convert("America/New_York")
    data.index = data.index.tz_localize(None)

    if hasattr(data.columns, "levels"):
        data.columns = data.columns.get_level_values(0)

    # so that indices like ^DJI and ^GSPC can be included in Intraday.txt
    if ticker.startswith("^"):
        filename = ticker[1:] + "-i.csv"
        print(f"{ticker[1:]}")
    else:
        filename = ticker + "-i.csv"
        print(f"{ticker}")
    filepath = data_folder / filename
    data.to_csv(filepath)

    # give server more time to process requests
    time.sleep(2)