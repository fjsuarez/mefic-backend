from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime

# Stock Price Data Model
class StockPrice(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    
class StockHistoryResponse(BaseModel):
    symbol: str
    company_name: str
    data: List[StockPrice]

# Financial Metrics Model
class FinancialMetrics(BaseModel):
    symbol: str
    company_name: str
    pe_ratio: Optional[float] = None
    roe: Optional[float] = None  # Return on Equity (%)
    roa: Optional[float] = None  # Return on Assets (%)
    dividend_score: Optional[float] = None
    dividend_yield: Optional[float] = None  # (%)
    payout_ratio: Optional[float] = None  # (%)

# Technical Indicators Model
class TechnicalIndicators(BaseModel):
    symbol: str
    sma_20: Optional[float] = None  # Simple Moving Average (20 days)
    sma_50: Optional[float] = None  # Simple Moving Average (50 days)
    sma_200: Optional[float] = None  # Simple Moving Average (200 days)
    ema_20: Optional[float] = None  # Exponential Moving Average (20 days)
    rsi_14: Optional[float] = None  # Relative Strength Index (14 days)
    macd: Optional[float] = None  # Moving Average Convergence Divergence
    macd_signal: Optional[float] = None
    bollinger_upper: Optional[float] = None
    bollinger_lower: Optional[float] = None
    
# Risk Metrics Model
class RiskMetrics(BaseModel):
    symbol: str
    beta: float
    volatility: float  # (%)
    sharpe_ratio: float
    max_drawdown: float  # (%)

# Portfolio Metrics Model
class PortfolioMetrics(BaseModel):
    symbol: str
    annual_return: float  # (%)
    alpha: float  # (%)
    info_ratio: float
    tracking_error: float  # (%)

# Stock Comparison Row Model
class StockComparisonItem(BaseModel):
    symbol: str
    company: str
    pe_ratio: Optional[float] = None
    roe: Optional[float] = None  # (%)
    roa: Optional[float] = None  # (%)
    dividend_score: Optional[float] = None
    dividend_yield: Optional[float] = None  # (%)
    payout_ratio: Optional[float] = None  # (%)
    
class StockComparisonResponse(BaseModel):
    stocks: List[StockComparisonItem]

# Date Range Request Model
class DateRangeRequest(BaseModel):
    start_date: date
    end_date: date = Field(default_factory=date.today)

# Error Response Model
class ErrorResponse(BaseModel):
    detail: str
