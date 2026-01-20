class Spread:
    def __init__(self,
                 coin_name: str,
                 exchange_buy: str,
                 exchange_sell: str,
                 price_buy: float,
                 price_sell: float,
                 spread_absolute: float,
                 spread_percent: float,
                 is_deposit_enabled: bool,
                 is_withdrawal_enabled: bool) -> None:
        self._coin_name = coin_name
        self._exchange_buy = exchange_buy
        self._exchange_sell = exchange_sell
        self._price_buy = price_buy
        self._price_sell = price_sell
        self._spread_absolute = spread_absolute
        self._spread_percent = spread_percent
        self._is_deposit_enabled = is_deposit_enabled
        self._is_withdrawal_enabled = is_withdrawal_enabled

    @property
    def to_json(self) -> dict:
        return {'coin_name': self._coin_name,
                'exchange_buy': self._exchange_buy,
                'exchange_sell': self._exchange_sell,
                'price_buy': self._price_buy,
                'price_sell': self._price_sell,
                'spread_absolute': self._spread_absolute,
                'spread_percent': self._spread_percent,
                'is_deposit_enabled': self._is_deposit_enabled,
                'is_withdrawal_enabled': self._is_withdrawal_enabled
                }

    @property
    def coin_name(self) -> str:
        return self._coin_name

    @property
    def exchange_buy(self) -> str:
        return self._exchange_buy

    @property
    def exchange_sell(self) -> str:
        return self._exchange_sell

    @property
    def price_buy(self) -> float:
        return self._price_buy

    @property
    def price_sell(self) -> float:
        return self._price_sell

    @property
    def spread_absolute(self) -> float:
        return self._spread_absolute

    @property
    def spread_percent(self) -> float:
        return self._spread_percent

    @property
    def is_deposit_enabled(self) -> bool:
        return self._is_deposit_enabled

    @property
    def is_withdraw_enabled(self) -> bool:
        return self._is_withdrawal_enabled
