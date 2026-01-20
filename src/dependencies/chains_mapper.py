from fastapi import Request

from src.chains.mapper import ChainsMapper


def get_chains_mapper(request: Request) -> ChainsMapper:
    return request.app.state.chains_mapper
