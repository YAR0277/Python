import yfinance as yf
import pandas as pd
import time
from pathlib import Path
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

# script directory ... Project/Python
base_path = Path(__file__).resolve().parent

# Equity.txt file path
tickers_file_path = base_path.parent / "Batch" / "Equity.txt"

# ingest tickers from file
with open(tickers_file_path, "r") as file:
    tickers = [line.strip() for line in file if line.strip()]

# download tickers to data folder
data_folder = base_path.parent.parent / "data" / "finance" / "equity"
for ticker in tickers:
    data = yf.download(ticker,period="3mo",interval="1d")

    if hasattr(data.columns, "levels"):
        data.columns = data.columns.get_level_values(0)

    filename = ticker + "-d.csv"
    filepath = data_folder / filename
    data.to_csv(filepath)

    # give server more time to process requests
    time.sleep(2)