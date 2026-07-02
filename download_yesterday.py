from pathlib import Path
from download_util import download_list
from download_util import intraday_filename
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

download_list(
    ticker_files=[
        base_path.parent / "Batch" / "ETF.txt",
        base_path.parent / "Batch" / "Equity.txt",
    ], 
    output_folder=base_path.parent.parent / "data" / "finance" / "intraday",
    filename_func = intraday_filename,
    period=None,
    interval="1m",
    start=start,
    end=end,
)
