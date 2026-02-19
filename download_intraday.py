import yfinance as yf
import pandas as pd
import time
from pathlib import Path
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

# script directory ... Project/Python
base_path = Path(__file__).resolve().parent

# ETF.txt file path
tickers_file_path = base_path.parent / "Batch" / "Intraday.txt"

# ingest tickers from file
with open(tickers_file_path, "r") as file:
    tickers = [line.strip() for line in file if line.strip()]

# download tickers to data folder
data_folder = base_path.parent.parent / "data" / "finance" / "etf"
for ticker in tickers:
    data = yf.download(ticker,period="1d",interval="5m")

    data = data.tz_convert("America/New_York")
    data.index = data.index.tz_localize(None)

    if hasattr(data.columns, "levels"):
        data.columns = data.columns.get_level_values(0)

    filename = ticker + "-i.csv"
    filepath = data_folder / filename
    data.to_csv(filepath)

    # give server more time to process requests
    time.sleep(2)