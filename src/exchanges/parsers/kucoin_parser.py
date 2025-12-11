from src.coins.info import CoinInfo
from src.coins.prices import CoinPrices
from src.exchanges.parsers.abstract import BaseParser


class KuCoinParser(BaseParser):
    """KuCoin API parser"""

    def _create_coin_info(self, **kwargs) -> CoinInfo:
        return CoinInfo(
            chain=kwargs['chain'],
            contract=kwargs['contract'],
            is_deposit_enabled=kwargs['is_deposit'],
            is_withdraw_enabled=kwargs['is_withdraw']
        )

    def _create_coin_prices(self, **kwargs) -> CoinPrices:
        return CoinPrices(
            ask=kwargs['ask'],
            bid=kwargs['bid']
        )
