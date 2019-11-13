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
from datetime import datetime

# Scripts
from src.base import get_paths, get_file

# ---
# Functions and classes
# ---

# Todo: Get real time quote:
# src https://github.com/pydata/pandas-datareader/issues/44

def get_data(stocks, source, metric="Close", start='2016-01-01', end=None):
    """
    Get price values from source

    :param stocks: list
    :param metrics: str., optional
    :param source: str., optional
    :param start: str., optional
    :param end: str., optional
    :return: pandas.DataFrame
    """
    if source.lower() == "yahoo":
        stocks = [item + ".AX" for item in stocks]

    else:
        msg = "The source needs to be yahoo."
        raise ValueError(msg)

    print("Loading data from {}.".format(source))

    if not end:
        end = str(datetime.now().date())

    downloaded_data = yf.download(stocks, start=start, end=end)[metric]

    columns = pd.MultiIndex.from_product([stocks, [metric]])
    data = pd.DataFrame(columns=columns, index=downloaded_data.index)

    for share in downloaded_data.columns:
        data.loc[:, (share, metric)] = downloaded_data.loc[:, share].values

    data.dropna(how="all", inplace=True)
    data.sort_index(ascending=True, inplace=True)

    return data


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


def save_data(data, filename=None, path=None):
    """
    Save pandas.dataframe to folder

    :param data: pandas.DataFrame
    :param filename: str., optional
    :param path: str., optional
    :return:
    """

    if not path:
        paths = get_paths()
        path = paths.get("data").get("interim")

    if not filename:
        filename = str(datetime.now().date()) + ".csv"

    full_filename = os.path.join(path, filename)
    data.to_csv(full_filename)

    return None


def main(stocks, source="yahoo"):
    """
    Generates dataframe with price values of selected stocks

    :param stocks: list
    :param source: str., optinal
    :return: pandas.dataframe
    """

    """
    Get stock prices 
    """
    data = get_data(stocks, source)

    """
    Clean data
    """
    data = input_data(data)

    """
    Return/save the data
    """

    save_data(data, filename=None, path=None)

    return data


if __name__ == "__main__":

    portfolio = ["WES", 'QBE']

    candidates = ['CUV', 'ALT', "AEF", "AGL", "COH", "BHP", "ALU", "ORG", "CSL",
                  "VAS", "WOW", "A2M", "MVF"]

    portfolio.extend(candidates)

    main(portfolio)

