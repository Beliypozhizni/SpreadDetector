from fastapi import Request

def get_exchange_names(request: Request) -> list[str]:
    mgr = request.app.state.exchange_manager
    return list(mgr.exchanges.keys())
