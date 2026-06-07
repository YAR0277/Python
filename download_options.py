import yfinance as yf
import pandas as pd
import time
from pathlib import Path
from datetime import datetime

# timestamp
today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# script directory ... Project/Python
base_path = Path(__file__).resolve().parent

# Equity.txt file path
tickers_file_path = base_path.parent / "Batch" / "Equity.txt"

# ingest tickers from file
with open(tickers_file_path, "r") as file:
    tickers = [line.strip() for line in file if line.strip()]

# download tickers to data folder
data_folder = base_path.parent.parent / "data" / "finance" / "options"
data_folder.mkdir(parents=True, exist_ok=True)

for ticker in tickers:

    try:

        tickerObj = yf.Ticker(ticker)

        all_options = []

        expirations = tickerObj.options

        if not expirations:
            print(f"{ticker}: No options available")
            continue

        for expiry in expirations:

            chain = tickerObj.option_chain(expiry)

            calls = chain.calls.copy()
            calls["expiration"] = expiry
            calls["optionType"] = "CALL"

            puts = chain.puts.copy()
            puts["expiration"] = expiry
            puts["optionType"] = "PUT"

            all_options.extend([calls, puts])
            if not all_options:
                print(f"{ticker}: No option contracts found")
                continue

        options_df = pd.concat(all_options, ignore_index=True)
        options_df["downloadDate"] = today        

        filename = f"{ticker}-o.csv"
        options_df.to_csv(data_folder / filename, index=False)
        print(f"{ticker}: saved {len(options_df)} contracts")

    except Exception as e:
        print(f"{ticker}: {e}")
    
    # give server more time to process requests
    time.sleep(2)