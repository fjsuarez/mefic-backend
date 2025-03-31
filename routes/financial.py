from fastapi import APIRouter, HTTPException
from services.financial_service import FinancialService
from services.stock_service import StockService
from models import FinancialMetrics, StockComparisonResponse, StockComparisonItem

router = APIRouter(
    prefix="/financial",
    tags=["financial"],
    responses={404: {"description": "Not found"}}
)

@router.get("/metrics/{symbol}", response_model=FinancialMetrics)
async def get_financial_metrics(symbol: str):
    """Get key financial metrics for a specific stock."""
    stocks = await StockService.get_available_stocks()
    
    if symbol not in stocks:
        raise HTTPException(status_code=404, detail=f"Stock with symbol {symbol} not found")
    
    try:
        metrics = await FinancialService.get_financial_metrics(symbol)
        
        return FinancialMetrics(
            symbol=symbol,
            company_name=stocks[symbol],
            **metrics
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/comparison", response_model=StockComparisonResponse)
async def get_stock_comparison():
    """Get comparison of key financial metrics for all stocks."""
    try:
        stocks = await StockService.get_available_stocks()
        comparison_data = await FinancialService.get_all_stocks_comparison(stocks)
        
        comparison_items = []
        for item in comparison_data:
            comparison_items.append(
                StockComparisonItem(
                    symbol=item["symbol"],
                    company=item["company"],
                    pe_ratio=item.get("pe_ratio"),
                    roe=item.get("roe"),
                    roa=item.get("roa"),
                    dividend_score=item.get("dividend_score"),
                    dividend_yield=item.get("dividend_yield"),
                    payout_ratio=item.get("payout_ratio")
                )
            )
        
        return StockComparisonResponse(stocks=comparison_items)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))