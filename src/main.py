import src.data.make_dataset as md
import src.features.build_features as bf

if __name__ == "__main__":

    portfolio = ["WES", 'QBE']

    candidates = ['CUV', 'ALT', "AEF", "AGL", "COH", "BHP", "ALU", "ORG", "CSL",
                  "VAS", "WOW", "A2M", "MVF"]

    portfolio.extend(candidates)

    data = md.main(portfolio)

    data = bf.get_trade_points(data, ("WES.AX", "Close"))

    print(data)