import os

from datetime import datetime

import src.data.make_dataset as md
import src.features.build_features as bf
import src.base as base

def post_processing(data):

    latest_day = max(data.index)
    mask = data.index == latest_day

    columns = [feature for feature in data.columns.values if feature[1] ==
               "Trade"]

    subset = data.loc[mask, columns].T

    mask = subset != "Hold"

    trade_shares = subset[mask].dropna()

    if not trade_shares.empty:
        msg = "Trade the shares {}.".format(trade_shares.index)
        trade = True

    else:
        msg = "No trading today :("
        trade = False

    print(msg)

    return trade

if __name__ == "__main__":

    paths = base.get_paths()

    portfolio = ["WES", 'QBE']

    candidates = ['CUV', 'ALT', "AEF", "AGL", "COH", "BHP", "ALU", "ORG", "CSL",
                  "VAS", "WOW", "A2M", "MVF"]

    portfolio.extend(candidates)

    data = md.main(portfolio)

    data = bf.get_trade_points(data)

    filename = str(datetime.now().date()) + ".csv"
    full_filename = os.path.join(paths.get("data").get("processed"), filename)

    data.to_csv(full_filename)

    post_processing(data)