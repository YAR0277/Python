import time
import yfinance as yf

def download_list(
        ticker_files, 
        output_folder, 
        filename_func=None,
        process_func=None,
        period="3mo",
        interval="1d",
        start=None,
        end=None,
        prepost=False,
        auto_adjust=False,
        progress=False,
        pause=0.5,
):

    output_folder.mkdir(parents=True, exist_ok=True)

    if not isinstance(ticker_files, (list, tuple)):
        ticker_files = [ticker_files]

    for ticker_file in ticker_files:

        if not ticker_file.exists():
            print(f"Missing file: {ticker_file}")
            return

        with open(ticker_file) as f:
            tickers = [line.strip() for line in f if line.strip()]

        for ticker in tickers:

            try:
                data = yf.download(
                    ticker,
                    period=period,
                    interval=interval,
                    start=start,
                    end=end,
                    prepost=prepost,
                    auto_adjust=auto_adjust,
                    progress=progress,
                )

                if hasattr(data.columns, "levels"):
                    data.columns = data.columns.get_level_values(0)

                if process_func is not None:
                    data = process_func(data)

                if filename_func is None:
                    filename = f"{ticker}-d.csv"
                else:
                    filename = filename_func(ticker)

                data.to_csv(output_folder / filename)

                display_name = ticker.lstrip("^")
                print(display_name)

            except Exception as e:
                print(f"{ticker}: {e}")

            time.sleep(pause)

def process_intraday(data):

    data = data.tz_convert("America/New_York")
    data.index = data.index.tz_localize(None)

    return data.between_time("09:30", "16:00")

def process_premarket(data):

    data = data.tz_convert("America/New_York")
    data.index = data.index.tz_localize(None)

    return data.between_time("04:00", "09:30")

def intraday_filename(ticker):
    return f"{ticker.lstrip('^')}-i.csv"