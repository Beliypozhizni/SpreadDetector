from src.coins.aggregator import CoinAggregator
from src.spreads.spread import Spread
from src.spreads.storage import SpreadStorage
from src.utils.logger import logger


class SpreadCalculator:
    def __init__(self, coin_aggregator: CoinAggregator, spread_storage: SpreadStorage):
        self.coin_aggregator = coin_aggregator
        self.spread_storage = spread_storage
        self.coin_aggregator.on_coins_added(self.calculate_all)
        print('Spread calculator initialized')

    async def calculate_all(self) -> None:
        try:
            spreads: list[Spread] = []
            for chain_contract, exchanges in self.coin_aggregator.coins.items():
                for exchange_buy, coin_data_buy in exchanges.items():
                    for exchange_sell, coin_data_sell in exchanges.items():
                        ask = coin_data_buy.coin_prices.ask
                        bid = coin_data_sell.coin_prices.bid

                        if bid <= ask:
                            continue

                        coin_name = coin_data_buy.coin_info.name
                        spread_absolute = bid - ask
                        spread_percent = (spread_absolute / bid) * 100
                        is_withdrawal_enabled = coin_data_buy.coin_info.is_withdraw_enabled
                        is_deposit_enabled = coin_data_sell.coin_info.is_deposit_enabled

                        spread = Spread(
                            coin_name=coin_name,
                            exchange_buy=exchange_buy,
                            exchange_sell=exchange_sell,
                            price_buy=ask,
                            price_sell=bid,
                            spread_absolute=spread_absolute,
                            spread_percent=spread_percent,
                            is_deposit_enabled=is_deposit_enabled,
                            is_withdrawal_enabled=is_withdrawal_enabled,
                        )

                        spreads.append(spread)

            await self.spread_storage.add_spreads(spreads)

        except Exception as e:
            logger.error(e)
