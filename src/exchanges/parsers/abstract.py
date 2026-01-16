from abc import ABC, abstractmethod
from typing import Any

from src.utils.logger import logger


class BaseParser(ABC):
    """Abstract exchange data parser"""

    def __init__(self, config: 'ExchangeConfig'):
        self.config = config
        self._json_keys = config.json_keys

    def _get_nested_value(self, data: dict, key_path: str) -> Any:
        """Get value by path 'key.subkey.subsubkey'"""
        keys = key_path.split('.')
        current = data
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key)
            else:
                return None
        return current

    def parse_info(self, data: dict) -> dict[str, list]:
        """Parsing coin information"""
        keys = self._json_keys.get('info', {})
        result = {}
        invalid_count = 0

        currencies = self._get_nested_value(data, keys.get('list_key', 'data'))
        if not isinstance(currencies, list):
            logger.error(f"{self.config.name}: Expected list, got {type(currencies).__name__}")
            return {}

        for currency in currencies:
            name = currency.get(keys.get('coin_name', 'currency'))
            chains = currency.get(keys.get('chains_key', 'chains'))

            if not name or not chains or not isinstance(chains, list):
                invalid_count += 1
                continue

            valid_chains = []
            for chain_info in chains:
                chain = chain_info.get(keys.get('chain_name', 'chainName'))
                contract = chain_info.get(keys.get('contract', 'contractAddress'))
                contract = self.config.processors.get('contract_processor', lambda x: x or '')(contract)
                is_deposit = chain_info.get(keys.get('deposit_enabled', 'isDepositEnabled'))
                is_withdraw = chain_info.get(keys.get('withdraw_enabled', 'isWithdrawEnabled'))

                if not chain or is_deposit is None or is_withdraw is None:
                    continue

                valid_chains.append(self._create_coin_info(
                    name=name,
                    chain=chain,
                    contract=contract,
                    is_deposit=is_deposit,
                    is_withdraw=is_withdraw
                ))

            if valid_chains:
                result[name] = valid_chains

        if invalid_count:
            logger.warning(f"{self.config.name}: Skipped {invalid_count} invalid currencies")

        return result

    def parse_prices(self, data: dict) -> dict[str, Any]:
        """Parsing prices"""
        keys = self._json_keys.get('prices', {})
        result = {}
        skipped_count = 0

        tickers = self._get_nested_value(data, keys.get('list_key', 'ticker'))
        if not isinstance(tickers, list):
            logger.error(f"{self.config.name}: Expected list, got {type(tickers).__name__}")
            return {}

        for ticker in tickers:
            symbol = ticker.get(keys.get('symbol', 'symbol'), '')

            if 'USDT' not in symbol:
                skipped_count += 1
                continue

            # Применяем обработчик символа если есть
            symbol_processor = self.config.processors.get('symbol_processor')
            name = symbol_processor(symbol) if symbol_processor else symbol

            ask_str = ticker.get(keys.get('ask_price', 'ask'))
            bid_str = ticker.get(keys.get('bid_price', 'bid'))

            if not ask_str or not bid_str:
                skipped_count += 1
                continue

            try:
                ask_price = float(ask_str)
                bid_price = float(bid_str)

                if ask_price <= 0 or bid_price <= 0:
                    skipped_count += 1
                    continue

                result[name] = self._create_coin_prices(
                    ask=ask_price,
                    bid=bid_price
                )

            except (ValueError, TypeError):
                skipped_count += 1
                continue

        logger.info(f"{self.config.name}: Loaded {len(result)} prices, skipped {skipped_count} tickers")
        return result

    @abstractmethod
    def _create_coin_info(self, **kwargs):
        """Create CoinInfo object"""
        pass

    @abstractmethod
    def _create_coin_prices(self, **kwargs):
        """Create CoinPrices object"""
        pass
