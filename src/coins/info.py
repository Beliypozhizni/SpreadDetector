from dataclasses import dataclass

@dataclass
class CoinInfo:
    chain: str
    contract: str
    is_deposit_enabled: bool
    is_withdraw_enabled: bool
