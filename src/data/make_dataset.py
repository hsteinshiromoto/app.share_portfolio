# ---
# Import
# ---

# Data Source Modules
from alpha_vantage.timeseries import TimeSeries

# Data Manipulation Modules
import pandas as pd

# Infrastructure Modules
import os
import warnings
from pathlib import Path
from datetime import datetime
import time
from glob import glob

# Scripts
from src.base import get_file

# ---
# Global Definitions
# ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
PATH_DATA = PROJECT_ROOT / "data"
PATH_DATA_RAW = PATH_DATA / "raw"
# ---
# Functions and classes
# ---

# Todo: Get real time quote:
# src https://github.com/pydata/pandas-datareader/issues/44

def get_data(portfolio: list, start_date: datetime=None,
             end_date: datetime=None):
    """
    Get price values from source

    :param portfolio:
    :param start_date:
    :param end_date:
    :return: pandas.DataFrame
    """

    if os.getenv("ALPHAVANTAGE_API_KEY") is not None:
        ts = TimeSeries(key=os.getenv("ALPHAVANTAGE_API_KEY"),
                        output_format="pandas", indexing_type='date')

    else:
        raise EnvironmentError(f"Expected environment variable "
                               f"ALPHAVANTAGE_API_KEY. Got "
                               f"{type(os.getenv('ALPHAVANTAGE_API_KEY'))}.")

    try:
        if end_date < start_date:
            msg = f"Expected start_date to be larger than end_date. " \
                  f"Got end_date={end_date} < start_date={start_date}."
            raise ValueError(msg)

    except TypeError:
        if (start_date == None) or (end_date == None):
            pass

        else:
            raise

    for stock in portfolio:

        print(f"Getting stock {stock}")

        time_start = datetime.now()
        data, meta_data = ts.get_daily(symbol=stock, outputsize='full')
        data.reset_index(inplace=True)
        data.rename(
            columns={column: column[3:].capitalize() if column != "date"
            else "Date" for column in data.columns.values},
            inplace=True)
        data["Symbol"] = stock

        try:
            df = df.append(data)

        except NameError:
            df = data.copy()

        time_diff = datetime.now() - time_start
        if time_diff.seconds <= 60:
            print(f"Waiting {60 - time_diff.seconds} seconds for next iteration "
                  f"...")
            time.sleep(60 - time_diff.seconds)

    if start_date:
        mask_start_date = df["Date"] >= start_date
        df = df.loc[mask_start_date, :]

    if end_date:
        mask_end_date = df["Date"] <= end_date
        df = df.loc[mask_end_date, :]

    return df


def input_data(data, missing_values_tolerance=5.0):
    # Todo: Create a config file and define missing_values_tolerance there
    """
    Input missing values with forward fill

    :param data: pandas.DataFrame
    :param missing_values_tolerance: float, optional
    :return: pandas.DataFrame
    """

    missing_data = data.isnull().sum().to_frame()

    new_column_name = "Count of Missing Values"

    missing_data.rename(columns={0: new_column_name}, inplace=True)
    missing_data = missing_data[missing_data[new_column_name] > 0]
    missing_data.loc[:, "%"] = missing_data[new_column_name] / data.shape[0] * 100.0

    if missing_data["%"].max() > missing_values_tolerance:
        msg = f"Tolerance of missing values is {missing_values_tolerance}%. " \
              f"Values could not be fetched:\n{missing_data}."
        raise ValueError(msg)

    data.fillna(method="ffill", inplace=True)

    return data


def load_previous_dataset(filename=None, path=None):
    # For future use
    """
    Get the latest date of the existing dataset

    :param filename: str., optional
    :param path: str., optional

    :return date: datetime
    """

    if not path:
        paths = get_paths()
        path = paths.get("data").get("interim")

    try:
        if not filename:
            filename = get_file(path, pattern=None, extension=".csv", latest=True)

    except IOError:
        msg = "Expected data set in {}. Found none.".format(path)
        warnings.warn(msg)
        data = None

    else:
        full_filename = os.path.join(path, filename)
        data = pd.read_csv(full_filename, index_col=0, header=[0,1])
        data.index = pd.to_datetime(data.index)

    return data


def save_data(data: pd.DataFrame, filename: str="raw.csv",
              path=PATH_DATA_RAW, as_new_file: bool=False):
    """
    Save data set

    :param data: pd.DataFrame
    :param filename: str., optional
    :param path:
    :param as_new_file: bool., optional
    :return: None
    """

    if not as_new_file:
        list_of_files = glob(str(path / "*.csv"))
        filename = max(list_of_files, key=os.path.getctime)
        filename = os.path.basename(filename)

    data.to_csv(str(path / filename), index=False)

    return None


def main(portfolio):
    """
    Generates dataframe with price values of selected stocks

    :param portfolio: list
    :return: pandas.dataframe
    """

    """
    Get stock prices 
    """
    data = get_data(portfolio)

    """
    Clean data
    """
    data = input_data(data)

    """
    Return/save the data
    """

    timestamp = str(datetime.now().date())
    save_data(data, as_new_file=True)
    # save_data(data, filename=None, path=None)

    return data


if __name__ == "__main__":

    share_code_list = ["WES", 'QBE', 'CUV', "AGL", "COH", "BHP", "CSL", "VAS",
                       "WOW", "A2M", "MVF"]
    share_code_list = ["IVV", "NDQ" , "VAP", "VAS", "CSL", "WES", "F100"]
    shares_list = [share + ".AX" for share in share_code_list]

    main(shares_list)

