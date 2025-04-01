from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional
from services.screener_service import ScreenerService
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/screener",
    tags=["screener"],
    responses={404: {"description": "Not found"}}
)

class ScreenerWeights(BaseModel):
    pe_ratio: float = Field(0.25, ge=0.0, le=1.0)
    roe: float = Field(0.25, ge=0.0, le=1.0)
    roa: float = Field(0.25, ge=0.0, le=1.0)
    dividend_yield: float = Field(0.25, ge=0.0, le=1.0)

class ScreenerResponse(BaseModel):
    stocks: List[Dict]

@router.post("/", response_model=ScreenerResponse)
async def get_screener_data(weights: Optional[ScreenerWeights] = None):
    """Get stock screener data with custom weights for financial metrics"""
    try:
        if weights:
            # Convert Pydantic model to dict
            weights_dict = weights.dict()
        else:
            weights_dict = None
            
        stocks = await ScreenerService.get_screener_data(weights_dict)
        return {"stocks": stocks}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 