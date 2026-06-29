import yfinance as yf
import pandas as pd
import time
from pathlib import Path
from datetime import datetime, timedelta

today = datetime.now().date()

numDays=5
# Yahoo intraday limits:
# 1m -> max 7 days
# 5m/15m/etc -> max 60 days
# so we over-request calendar days safely
calendarDays = int(numDays*2.5)

end = datetime.combine(today,datetime.min.time())
start = end - timedelta(days=calendarDays)

# script directory ... Project/Python
base_path = Path(__file__).resolve().parent

# download tickers to data folder
data_folder = base_path.parent.parent / "data" / "finance" / "extended"
data_folder.mkdir(parents=True, exist_ok=True)

# ticker file paths
equity_file_path = base_path.parent / "Batch" / "Equity.txt"
etf_file_path = base_path.parent / "Batch" / "ETF.txt"

for tickers_file_path in [equity_file_path, etf_file_path]:

    if not tickers_file_path.exists():
        print(f"Missing file: {tickers_file_path}")
        continue

    # ingest tickers from file
    with open(tickers_file_path, "r") as file:
        tickers = [line.strip() for line in file if line.strip()]

    for ticker in tickers:

        try:

            data = yf.download(
                ticker,
                start=start,
                end=end,
                interval="5m",
                prepost=True,
                auto_adjust=False,
                progress=False
            )

            # get a list of trading dates
            tradingDates = sorted(pd.unique(data.index.date))

            # keep only last numDays trading dates
            lastDates = tradingDates[-numDays:]

            # filter data on lastDates
            mask = pd.Index(data.index.date).isin(lastDates)
            data = data[mask]

            data = data.tz_convert("America/New_York")
            data.index = data.index.tz_localize(None)

            if hasattr(data.columns, "levels"):
                data.columns = data.columns.get_level_values(0)

            filename = ticker + "-e.csv"
            filepath = data_folder / filename
            data.to_csv(filepath)

            print(f"{ticker}")

        except Exception as e:
            print(f"{ticker}: {e}")

        # give server more time to process requests
        time.sleep(2)