# ---
# Import
# ---


import os
import time
import warnings
from datetime import datetime
from glob import glob
from pathlib import Path

import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from typeguard import typechecked

# ---
# Global Definitions
# ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
PATH_DATA = PROJECT_ROOT / "data"
PATH_DATA_RAW = PATH_DATA / "raw"

# ---
# Functions and classes
# ---

#!TODO: Get real time quote:
# src https://github.com/pydata/pandas-datareader/issues/44


@typechecked
def get_stock_data(stock: str) -> pd.DataFrame:
    """
    Get data from a specific stock

    Args:
        stock (str): Stock symbol

    Returns:
        data (pd.DataFrame): Stock data

    Raises:
        EnvironmentError: Undefined API key

    Example:
        >>> stock = "IVV"
        >>> data = get_stock_data(stock)
        >>> isinstance(data, pd.DataFrame)
        True
        >>> data["Symbol"].drop_duplicates()[0] == stock
        True
    """

    if not os.getenv("ALPHAVANTAGE_API_KEY"):
        raise EnvironmentError(f"Expected environment variable "
                               f"ALPHAVANTAGE_API_KEY. Got "
                               f"{type(os.getenv('ALPHAVANTAGE_API_KEY'))}.")

    # 1. Instantiate time series object from alpha vantage
    ts = TimeSeries(key=os.getenv("ALPHAVANTAGE_API_KEY"),
                    output_format="pandas", indexing_type='date')

    # 2. Get stock
    data, meta_data = ts.get_daily(symbol=stock, outputsize='full')

    # 3. Format column names
    data.rename(columns={column: column[3:].capitalize() if column != "date"
                else "Date" for column in data.columns.values}, inplace=True
                )
    data["Symbol"] = stock

    data.index.name = 'Date'

    return data


@typechecked
def get_portfolio(portfolio: list[str]) -> pd.DataFrame:
    """Get stocks info

    Args:
        portfolio (list[str]): List of symbols

    Returns:
        pd.DataFrame: [description]

    Example:
        >>> portfolio = ["IVV", "CSL"]
        >>> data = get_portfolio(portfolio)
        >>> isinstance(data, pd.DataFrame)
        True
        >>> len(set(data["Symbol"].drop_duplicates().values).symmetric_difference(set(portfolio))) == 0
        True
    """
    # Iterate over each stock
    for stock in portfolio:
        time_start = datetime.now()

        try:
            data = pd.concat([data, get_stock_data(stock)])

        except NameError:
            data = get_stock_data(stock)
        
        time_diff = datetime.now() - time_start
        if time_diff.seconds <= 61:
            # Wait, at least, 60s to get the next stock
            time.sleep(61 - time_diff.seconds)

    return data


@typechecked
def get_momentum(data: pd.DataFrame, metric: str="Close", short_term: int=30,
                long_term: int=90) -> pd.DataFrame:
    """Calculate the Exponential Weighted Mean (EWM) of a given metric

    Args:
        data (pd.DataFrame): Data frame containing prices
        metric (str, optional): Metric to be used to calculate the EWM. Defaults to "Close".
        short_term (int, optional): Number of days in short term momentum. Defaults to 30.
        long_term (int, optional): Number of days in long term momentum. Defaults to 90.

    Raises:
        ValueError: long_term must be larger than short_term 
        KeyError: Expected metric to be either Open, Close, High or Low

    Returns:
        pd.DataFrame: Data frame with 
    """

    if short_term >= long_term:
        msg = f"Expected short_term < long_term. Got {short_term} >= {long_term}."
        raise ValueError(msg)

    try:
        data[f"Short_Term_{metric}"] = data[metric].ewm(span=short_term, adjust=False).mean()
        data[f"Long_Term_{metric}"] = data[metric].ewm(span=long_term, adjust=False).mean()

    except KeyError:
        msg = f"Expected metric to be either Open, Close, High or Low. Got {metric}."
        raise KeyError(msg)

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


# def load_previous_dataset(filename=None, path=None):
#     # For future use
#     """
#     Get the latest date of the existing dataset
#
#     :param filename: str., optional
#     :param path: str., optional
#
#     :return date: datetime
#     """
#
#     if not path:
#         paths = get_paths()
#         path = paths.get("data").get("interim")
#
#     try:
#         if not filename:
#             filename = get_file(path, pattern=None, extension=".csv", latest=True)
#
#     except IOError:
#         msg = "Expected data set in {}. Found none.".format(path)
#         warnings.warn(msg)
#         data = None
#
#     else:
#         full_filename = os.path.join(path, filename)
#         data = pd.read_csv(full_filename, index_col=0, header=[0,1])
#         data.index = pd.to_datetime(data.index)
#
#     return data


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
    # data = get_data(portfolio)

    """
    Clean data
    """
    # data = input_data(data)

    """
    Return/save the data
    """

    # timestamp = str(datetime.now().date())
    # save_data(data, as_new_file=True)
    # save_data(data, filename=None, path=None)

    pass


if __name__ == "__main__":

    share_code_list = ["WES", 'QBE', 'CUV', "AGL", "COH", "BHP", "CSL", "VAS",
                       "WOW", "A2M", "MVF"]
    share_code_list = ["IVV", "NDQ" , "VAP", "VAS", "CSL", "WES", "F100"]
    shares_list = [share + ".AX" for share in share_code_list]

    main(shares_list)

