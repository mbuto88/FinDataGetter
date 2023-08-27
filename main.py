from stockfinderv2 import fetchStocksByMarketv2
from data_fetchy import fetch_data


def main():
    market = "nasdaq"
    all_symbols = fetchStocksByMarketv2(market)
    fetch_data(all_symbols)


if __name__ == "__main__":
    main()
