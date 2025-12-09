from dataclasses import dataclass

@dataclass
class CoinInfo:
    price: float
    is_deposit_enabled: bool
    is_withdraw_enabled: bool