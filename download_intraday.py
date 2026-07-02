from pathlib import Path
from download_util import download_list
from download_util import intraday_filename

# script directory ... Project/Python
base_path = Path(__file__).resolve().parent

download_list(
    ticker_files=[
        base_path.parent / "Batch" / "ETF.txt",
        base_path.parent / "Batch" / "Equity.txt",
    ], 
    output_folder=base_path.parent.parent / "data" / "finance" / "intraday",
    filename_func = intraday_filename,
    period="1d",
    interval="1m",
)
