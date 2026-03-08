import yfinance as yf
import pandas as pd
import time
from pathlib import Path
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

# script directory ... Project/Python
base_path = Path(__file__).resolve().parent

# ETF.txt file path
tickers_file_path = base_path.parent / "Batch" / "Premarket.txt"

# ingest tickers from file
with open(tickers_file_path, "r") as file:
    tickers = [line.strip() for line in file if line.strip()]

# download tickers to data folder
data_folder = base_path.parent.parent / "data" / "finance" / "intraday"
for ticker in tickers:
    data = yf.download(ticker,period="1d",interval="5m",prepost=True)

    data = data.tz_convert("America/New_York")
    data.index = data.index.tz_localize(None)

    if hasattr(data.columns, "levels"):
        data.columns = data.columns.get_level_values(0)

    # keep only premarket
    premarket = data.between_time("04:00", "09:30")

    filename = ticker + "-i.csv"
    filepath = data_folder / filename
    premarket.to_csv(filepath)

    # give server more time to process requests
    time.sleep(2)