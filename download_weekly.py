from pathlib import Path
from download_util import download_list
from download_util import weekly_filename

# script directory ... Project/Python
base_path = Path(__file__).resolve().parent

download_list(
    ticker_files=[
        base_path.parent / "Batch" / "Equity.txt"
        ], 
    output_folder=base_path.parent.parent / "data" / "finance" / "equity",
    filename_func = weekly_filename,
    period="2y",
    interval="1wk",
)

download_list(
    ticker_files=[
        base_path.parent / "Batch" / "ETF.txt"
        ], 
    output_folder=base_path.parent.parent / "data" / "finance" / "etf",
    filename_func = weekly_filename,
    period="2y",
    interval="1wk",
)

download_list(
    ticker_files=[
        base_path.parent / "Batch" / "Index.txt"
        ], 
    output_folder=base_path.parent.parent / "data" / "finance" / "index",
    filename_func = weekly_filename,
    period="2y",
    interval="1wk",
)