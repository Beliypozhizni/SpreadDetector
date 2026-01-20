from src.exchanges.base import ExchangeAbstract
from src.exchanges.configs.kucoin_config import KuCoinConfig
from src.exchanges.parsers.kucoin_parser import KuCoinParser


class KuCoinClient(ExchangeAbstract):
    CONFIG_CLASS = KuCoinConfig
    PARSER_CLASS = KuCoinParser
