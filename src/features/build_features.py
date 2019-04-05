import numpy as np

def moving_average(array, window):
    weights = np.repeat(1.0, window) / window
    moving_average = np.convolve(array, weights, 'valid')

    return moving_average


def calculate_trade_points(prices, mean_prices):
    """

    :param prices: 1-dimensional np.array
    :param mean_price: 1-dimensional np.array
    return np.array
    """
    difference = prices - mean_prices

    zero_indices = np.argwhere(np.nan_to_num(np.diff(np.sign(difference)))).flatten()

    buy_indices = np.intersect1d(zero_indices, np.where(difference < 0)[0])

    sell_indices = np.intersect1d(zero_indices, np.where(difference > 0)[0])

    return buy_indices, sell_indices


def get_trade_points(data, feature):

    # Todo: add for loops to run into each feature

    prices = data.loc[:, feature].values
    data.loc[:, (feature[0], "EWM")] = data.loc[:, feature].ewm(span=15, adjust=False).mean()
    mean = data.loc[:, (feature[0], "EWM")].values

    buy_indices, sell_indices = calculate_trade_points(prices, mean)

    mask_buy = data[feature].index[buy_indices]
    mask_sell = data[feature].index[sell_indices]

    data.loc[mask_buy, (feature[0], "Trade")] = "Buy"
    data.loc[mask_sell, (feature[0], "Trade")] = "Sell"
    data.loc[:, (feature[0], "Trade")].fillna(value="Hold", inplace=True)

    return data