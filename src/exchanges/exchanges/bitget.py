from src.exchanges.base import ExchangeAbstract
from src.exchanges.configs.bitget_config import BitgetConfig
from src.exchanges.parsers.bitget_parser import BitgetParser


class BitgetClient(ExchangeAbstract):
    CONFIG_CLASS = BitgetConfig
    PARSER_CLASS = BitgetParser
