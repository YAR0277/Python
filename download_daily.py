from pathlib import Path
from download_util import download_list

# script directory ... Project/Python
base_path = Path(__file__).resolve().parent

download_list(
    ticker_files=[
        base_path.parent / "Batch" / "Equity.txt"
        ], 
    output_folder=base_path.parent.parent / "data" / "finance" / "equity",
)

download_list(
    ticker_files=[
        base_path.parent / "Batch" / "ETF.txt"
        ], 
    output_folder=base_path.parent.parent / "data" / "finance" / "etf",
)

download_list(
    ticker_files=[
        base_path.parent / "Batch" / "Index.txt"
        ], 
    output_folder=base_path.parent.parent / "data" / "finance" / "index",
    filename_func=lambda ticker: f"{ticker.lstrip('^')}-d.csv",
)
