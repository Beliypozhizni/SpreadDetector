from dataclasses import dataclass


@dataclass
class CoinInfo:
    name: str
    chain: str
    contract: str
    is_deposit_enabled: bool
    is_withdraw_enabled: bool
