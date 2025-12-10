from src.coins.info import CoinInfo
from src.coins.prices import CoinPrices
from src.exchanges.base import ExchangeAbstract
from src.utils.logger import logger


class KuCoinClient(ExchangeAbstract):
    @property
    def base_url(self) -> str:
        return 'api.kucoin.com'

    @classmethod
    def name(cls) -> str:
        return 'KuCoin'

    async def get_info(self) -> dict[str, list[CoinInfo]] | None:
        data = await self._make_request('/api/v3/currencies')
        if not data:
            logger.error(f"Expected dict, got {type(data).__name__} ")
            return None

        currencies = data.get('data')
        if not isinstance(currencies, list):
            logger.error(f"Expected list of currencies, got {type(currencies).__name__}")
            return None

        result = {}
        invalid_count = 0

        for currency in currencies:
            name = currency.get('currency')
            chains = currency.get('chains')

            if not name or not chains or not isinstance(chains, list):
                invalid_count += 1
                continue

            valid_chains = []
            for chain_info in chains:
                chain = chain_info.get('chainName')
                contract = chain_info.get('contractAddress') or ''
                is_deposit = chain_info.get('isDepositEnabled')
                is_withdraw = chain_info.get('isWithdrawEnabled')

                if not chain or is_deposit is None or is_withdraw is None:
                    continue

                valid_chains.append(CoinInfo(
                    chain=chain,
                    contract=contract,
                    is_deposit_enabled=is_deposit,
                    is_withdraw_enabled=is_withdraw
                ))

            if valid_chains:
                result[name] = valid_chains

        if invalid_count:
            logger.warning(f"Skipped {invalid_count} invalid currencies")

        return result if result else None

    async def get_prices(self) -> dict[str, CoinPrices] | None:
        data = await self._make_request('/api/v1/market/allTickers')
        if not data:
            logger.error(f"Expected dict, got {type(data).__name__} ")
            return None

        tickers = data.get('data', {}).get('ticker')
        if not isinstance(tickers, list):
            logger.error(f"Expected list of tickers, got {type(tickers).__name__}")
            return None

        result = {}
        skipped_count = 0

        for ticker in tickers:
            symbol = ticker.get('symbol', '')

            if 'USDT' not in symbol:
                skipped_count += 1
                continue

            name = symbol.replace('-USDT', '')
            ask_str = ticker.get('sell')
            bid_str = ticker.get('buy')

            if not ask_str or not bid_str:
                skipped_count += 1
                continue

            try:
                ask_price = float(ask_str)
                bid_price = float(bid_str)

                if ask_price <= 0 or bid_price <= 0:
                    skipped_count += 1
                    continue

                result[name] = CoinPrices(ask=ask_price, bid=bid_price)

            except (ValueError, TypeError):
                skipped_count += 1
                continue

        logger.info(f"Loaded {len(result)} prices, skipped {skipped_count} tickers")
        return result if result else None
