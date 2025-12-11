from src.exchanges.configs.abstract import ExchangeConfig, EndpointType

BitgetConfig = ExchangeConfig(
    name="Bitget",
    base_url="api.bitget.com",
    endpoints={
        EndpointType.INFO: "/api/v2/spot/public/coins",
        EndpointType.PRICES: "/api/v2/spot/market/tickers"
    },
    json_keys={
        "info": {
            "list_key": "data",
            "coin_name": "coin",
            "chains_key": "chains",
            "chain_name": "chain",
            "contract": "contractAddress",
            "deposit_enabled": "rechargeable",
            "withdraw_enabled": "withdrawable"
        },
        "prices": {
            "list_key": "data",
            "symbol": "symbol",
            "ask_price": "askPr",
            "bid_price": "bidPr"
        }
    },
    processors={
        "symbol_processor": lambda s: s.replace('USDT', ''),
        "contract_processor": lambda c: c or ''
    }
)
