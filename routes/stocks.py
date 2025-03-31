from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Optional
from datetime import datetime, timedelta
from services.stock_service import StockService
from models import StockHistoryResponse, StockPrice

router = APIRouter(
    prefix="/stocks",
    tags=["stocks"],
    responses={404: {"description": "Not found"}}
)

@router.get("/available", response_model=Dict[str, str])
async def get_available_stocks():
    """Get a list of all available stocks with their symbols and names."""
    return await StockService.get_available_stocks()

@router.get("/{symbol}/history", response_model=StockHistoryResponse)
async def get_stock_history(
    symbol: str,
    period: str = Query("6M", description="Time period: 1M, 3M, 6M, 1Y, 2Y, 5Y"),
    start_date: Optional[datetime] = Query(None, description="Custom start date"),
    end_date: Optional[datetime] = Query(None, description="Custom end date")
):
    """Get historical price data for a stock."""
    stocks = await StockService.get_available_stocks()
    
    if symbol not in stocks:
        raise HTTPException(status_code=404, detail=f"Stock with symbol {symbol} not found")
    
    # Convert period to actual dates if custom dates not provided
    if not (start_date and end_date):
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
    
    try:
        df = await StockService.get_stock_data(symbol, start_date, end_date)
        
        # Convert to StockPrice objects
        stock_prices = []
        for date, row in df.iterrows():
            stock_prices.append(
                StockPrice(
                    date=date,
                    open=row['Open'],
                    high=row['High'],
                    low=row['Low'],
                    close=row['Close'],
                    volume=int(row['Volume'])
                )
            )
        
        return StockHistoryResponse(
            symbol=symbol,
            company_name=stocks[symbol],
            data=stock_prices
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))