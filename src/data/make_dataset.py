import pandas_datareader as pdr
import pandas as pd
import os

from datetime import datetime

from src.base import get_paths

def get_data(stocks, metrics=None, source='yahoo', start='2016-01-01', end=None):
    """

    :param stocks: list
    :param metrics: list, optional
    :param source: str., optional
    :param start: str., optional
    :param end: str., optional
    :return: pandas.DataFrame
    """

    default_metrics = ["High", "Low", "Open", "Close", "Adj Close", "Volume"]

    if not metrics:
        metrics = ["Close"]

    elif (len(set(default_metrics) - set(metrics)) == len(set(default_metrics))):
        msg = "Expected metrics to be in {0}. Got {1}.".format(default_metrics,
                                                               metrics)
        raise ValueError(msg)

    if not end:
        end = '{0}-{1}-{2}'.format(datetime.now().year, datetime.now().month,
                                   datetime.now().day)

    index = pd.date_range(datetime.strptime(start,"%Y-%m-%d"),
                          datetime.strptime(end, "%Y-%m-%d"), freq='D')
    columns = pd.MultiIndex.from_product([stocks, metrics])

    data = pd.DataFrame(columns=columns, index=index)

    for share in stocks:
        for metric in metrics:
            data.loc[:, (share, metric)] = pdr.DataReader(share,
                                                          data_source=source,
                                                          start=start, end=end)\
                [metric]

    data.dropna(how="all", inplace=True)
    data.sort_index(ascending=True, inplace=True)

    return data


def save_data(data, filename=None, path=None):
    """

    :param data: pandas.DataFrame
    :param filename: str., optional
    :param path: str., optional
    :return:
    """

    if not path:
        paths = get_paths()
        path = paths.get("data").get("raw")

    if not filename:
        filename = str(datetime.now().date())

    full_filename = os.path.join(path, filename)
    data.to_csv(full_filename, index=False)

    return None


if __name__ == "__main__":

    portfolio = ["WES", 'QBE']

    candidates = ['CUV', 'ALT', "AEF", "AGL", "COH", "BHP", "ALU", "ORG", "CSL",
                  "VAS", "WOW", "A2M", "MVF"]

    portfolio.extend(candidates)
    portfolio = [item + ".AX" for item in portfolio]

    data = get_data(portfolio)

    print(data.head())
    print(data.tail())

