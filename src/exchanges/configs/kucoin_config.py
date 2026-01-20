from src.exchanges.configs.abstract import ExchangeConfig, EndpointType

KuCoinConfig = ExchangeConfig(
    name="KuCoin",
    base_url="api.kucoin.com",
    endpoints={
        EndpointType.INFO: "/api/v3/currencies",
        EndpointType.PRICES: "/api/v1/market/allTickers"
    },
    json_keys={
        "info": {
            "list_key": "data",
            "coin_name": "currency",
            "chains_key": "chains",
            "chain_name": "chainName",
            "contract": "contractAddress",
            "deposit_enabled": "isDepositEnabled",
            "withdraw_enabled": "isWithdrawEnabled"
        },
        "prices": {
            "list_key": "data.ticker",
            "symbol": "symbol",
            "ask_price": "sell",
            "bid_price": "buy"
        }
    },
    processors={
        "symbol_processor": lambda s: s.replace('-USDT', ''),
        "contract_processor": lambda c: c or ''
    }
)
