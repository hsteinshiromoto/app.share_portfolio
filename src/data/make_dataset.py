import pandas_datareader as pdr
import pandas as pd
import os
import warnings
import fix_yahoo_finance as yf
yf.pdr_override()

from datetime import datetime

from src.base import get_paths, get_file

# Todo: Get real time quote:
# src https://github.com/pydata/pandas-datareader/issues/44

def get_data(stocks, source, metrics=None, start='2016-01-01', end=None):
    """
    Get price values from source

    :param stocks: list
    :param metrics: list, optional
    :param source: str., optional
    :param start: str., optional
    :param end: str., optional
    :return: pandas.DataFrame
    """
    print("Loading data from {}.".format(source))

    if not end:
        end = str(datetime.now().date())

    data = pdr.get_data_yahoo(stocks, start=start, end=end)["Close"]

    data.dropna(how="all", inplace=True)
    data.sort_index(ascending=True, inplace=True)

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


def load_previous_dataset(filename=None, path=None):
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


def main(stocks, source="yahoo"):
    """
    Generates dataframe with price values of selected stocks

    :param stocks: list
    :param source: str., optinal
    :return: pandas.dataframe
    """

    if source.lower() == "yahoo":
        stocks = [item + ".AX" for item in stocks]

    else:
        msg = "The source needs to be yahoo."
        ValueError(msg)

    paths = get_paths()

    """
    Get stock prices 
    """
    data = load_previous_dataset(filename=None, path=None)

    if data is not None:
        previous_stocks_list = [item[0] for item in data.columns.values.squeeze()]
        missing_stocks = set(stocks).symmetric_difference(set(previous_stocks_list))
        latest_date = data.index[-1].date()
        date_equal = latest_date != datetime.now().date()

        full_filename = paths.get("data").get("interim")
        full_filename = os.path.join(full_filename, "{}.csv".format(latest_date.strftime("%Y-%m-%d")))
        os.remove(full_filename)

        if date_equal & (len(missing_stocks) == 0):
            new_data = get_data(stocks, source, start=latest_date.strftime("%Y-%m-%d"))
            data = pd.concat([data, new_data])

    else:
        data = get_data(stocks, source)

    """
    Clean data
    """
    # Clean missing values
    # Todo: Create a config file and define missing_values_tolerance there
    missing_values_tolerance = 5
    missing_data = data.isnull().sum().to_frame()
    new_column_name = "Count of Missing Values"
    missing_data.rename(columns={0: new_column_name}, inplace=True)
    missing_data = missing_data[missing_data[new_column_name] > 0]
    missing_data.loc[:, "%"] = missing_data[new_column_name] / data.shape[0] * 100.0

    if missing_data["%"].max() > missing_values_tolerance:
        msg = "Values could not be fetched:\n{}.".format(missing_data)
        raise ValueError(msg)

    data.fillna(method="ffill", inplace=True)

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

    # print(load_latest_date(filename=None, path=None))
