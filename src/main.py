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

    return trade_shares

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

    trade_shares = post_processing(data)

    print(trade_shares)