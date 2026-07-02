from pathlib import Path
from download_util import download_list

# script directory ... Project/Python
base_path = Path(__file__).resolve().parent

download_list(
    ticker_files=[
        base_path.parent / "Batch" / "Index.txt"
        ], 
    output_folder=base_path.parent.parent / "data" / "finance" / "index",
    filename_func=lambda ticker: f"{ticker.lstrip('^')}-d.csv",
)
