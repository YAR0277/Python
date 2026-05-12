import yfinance as yf
import pandas as pd
import time
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

timestamp = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S")

# script directory ... Project/Python
base_path = Path(__file__).resolve().parent

# Equity.txt file path
tickers_file_path = base_path.parent / "Batch" / "Equity.txt"

# ingest tickers from file
with open(tickers_file_path, "r") as file:
    tickers = [line.strip() for line in file if line.strip()]

# Fields.txt file path
fields_file_path = base_path.parent / "Batch" / "Fields.txt"

# ingest fields from file
with open(fields_file_path, "r") as file:
    fields = [line.strip() for line in file if line.strip()]

# download tickers to data folder
rows = []
data_folder = base_path.parent.parent / "data" / "finance" / "fundamentals"

for ticker in tickers:

    obj = yf.Ticker(ticker)
    info = obj.info

    row = {}

    # timestamp first
    row["last_updated"] = timestamp

    # then fundamentals
    for field in fields:
        row[field] = info.get(field)

    df = pd.DataFrame([row])

    filename = ticker + ".csv"
    filepath = data_folder / filename
    df.to_csv(filepath, mode="a", index=False, header=not filepath.exists())

    # give server more time to process requests
    time.sleep(1)
