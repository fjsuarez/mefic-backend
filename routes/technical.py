from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from services.stock_service import StockService
from services.technical_service import TechnicalService
from models import TechnicalIndicators

router = APIRouter(
    prefix="/technical",
    tags=["technical"],
    responses={404: {"description": "Not found"}}
)

@router.get("/indicators/{symbol}", response_model=TechnicalIndicators)
async def get_technical_indicators(
    symbol: str,
    period: str = "6M"
):
    """Get technical indicators for a specific stock."""
    stocks = await StockService.get_available_stocks()
    
    if symbol not in stocks:
        raise HTTPException(status_code=404, detail=f"Stock with symbol {symbol} not found")
    
    try:
        # Convert period to actual dates
        end_date = datetime.now()
        date_ranges = {
            "1M": 30,
            "3M": 90,
            "6M": 180,
            "1Y": 365,
            "2Y": 730,
            "5Y": 1825
        }
        
        if period not in date_ranges:
            raise HTTPException(status_code=400, detail=f"Invalid period: {period}")
            
        start_date = end_date - timedelta(days=date_ranges[period])
        
        # Get stock data
        df = await StockService.get_stock_data(symbol, start_date, end_date)
        
        # Calculate technical indicators
        indicators = await TechnicalService.calculate_technical_indicators(df)
        
        return TechnicalIndicators(
            symbol=symbol,
            **indicators
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))