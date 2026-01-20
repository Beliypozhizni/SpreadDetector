from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.chains.mapper import ChainsMapper
from src.dependencies.chains_mapper import get_chains_mapper

router = APIRouter(prefix="/chains_map", tags=["Chains"])


class ChainMapIn(BaseModel):
    input_name: str
    desired_name: str


@router.get("/", status_code=status.HTTP_200_OK)
def get_chains_map(mapper: ChainsMapper = Depends(get_chains_mapper)):
    return mapper.get_aggregated_map()


@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_chain(payload: ChainMapIn, mapper: ChainsMapper = Depends(get_chains_mapper)):
    if not mapper.add(payload.input_name, payload.desired_name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already exists or invalid input")
    return {"message": "ok"}


@router.delete("/remove/{input_name}", status_code=status.HTTP_204_NO_CONTENT)
def remove_chain(input_name: str, mapper: ChainsMapper = Depends(get_chains_mapper)):
    if not mapper.remove(input_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
