from src.coins.aggregator import CoinAggregator


class SpreadCalculator:
    def __init__(self, coin_aggregator: CoinAggregator):
        self.coin_aggregator = coin_aggregator
