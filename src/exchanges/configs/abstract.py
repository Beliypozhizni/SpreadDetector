from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Any


class EndpointType(Enum):
    INFO = "info"
    PRICES = "prices"


@dataclass
class ExchangeConfig:
    """Exchange API configuration"""
    name: str
    base_url: str
    endpoints: dict[EndpointType, str]
    api_keys_required: bool = False
    needs_signature: bool = False
    timeout: int = 30
    json_keys: dict[str, dict[str, str]] = field(default_factory=dict)
    processors: dict[str, Callable[[Any], Any]] = field(default_factory=dict)
