from fastapi import APIRouter, HTTPException, Depends
from firebase_admin import firestore
from pydantic import BaseModel
from typing import List, Dict, Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.auth_service import verify_firebase_token
from services.stock_service import StockService
import logging

router = APIRouter(
    prefix="/user-portfolio",
    tags=["user-portfolio"],
    responses={404: {"description": "Not found"}}
)

security = HTTPBearer()

# Configure logging
logger = logging.getLogger(__name__)

# Models for request/response
class PortfolioStock(BaseModel):
    symbol: str
    allocation: float  # Percentage allocation
    purchase_price: Optional[float] = None
    purchase_date: Optional[str] = None

class UserPortfolio(BaseModel):
    stocks: List[PortfolioStock]

@router.get("/", response_model=UserPortfolio)
async def get_user_portfolio(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get the current user's portfolio"""
    try:
        logger.info("Portfolio request received")
        
        # Check if credentials are provided
        if not credentials:
            logger.error("No credentials provided")
            raise HTTPException(status_code=401, detail="No credentials provided")
            
        logger.info(f"Authorization header received with token length: {len(credentials.credentials)}")
        
        # Verify token and get user ID
        user_id = await verify_firebase_token(credentials.credentials)
        
        logger.info(f"Fetching portfolio for user: {user_id}")
        # Access Firestore
        db = firestore.client()
        portfolio_ref = db.collection('portfolios').document(user_id)
        portfolio = portfolio_ref.get()
        
        if not portfolio.exists:
            logger.info(f"No portfolio found for user: {user_id}, returning empty portfolio")
            return UserPortfolio(stocks=[])
        
        logger.info(f"Successfully retrieved portfolio for user: {user_id}")
        return UserPortfolio(stocks=portfolio.to_dict().get('stocks', []))
    except Exception as e:
        logger.error(f"Error in get_user_portfolio: {str(e)}")
        raise

@router.post("/", response_model=UserPortfolio)
async def update_user_portfolio(
    portfolio: UserPortfolio, 
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Update the entire portfolio"""
    user_id = await verify_firebase_token(credentials.credentials)
    
    # Validate all stock symbols
    stocks = await StockService.get_available_stocks()
    for stock in portfolio.stocks:
        if stock.symbol not in stocks:
            raise HTTPException(status_code=400, detail=f"Invalid stock symbol: {stock.symbol}")
    
    # Validate allocation percentages sum to approximately 100%
    total_allocation = sum(stock.allocation for stock in portfolio.stocks)
    if not (98 <= total_allocation <= 102):  # Allow small rounding errors
        raise HTTPException(status_code=400, detail=f"Total allocation must be 100%, got {total_allocation}%")
    
    # Update in Firestore
    db = firestore.client()
    portfolio_ref = db.collection('portfolios').document(user_id)
    portfolio_ref.set({'stocks': [stock.dict() for stock in portfolio.stocks]})
    
    return portfolio

@router.post("/add", response_model=UserPortfolio)
async def add_stock_to_portfolio(
    stock: PortfolioStock,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Add a stock to the portfolio"""
    user_id = await verify_firebase_token(credentials.credentials)
    
    # Validate stock symbol
    stocks = await StockService.get_available_stocks()
    if stock.symbol not in stocks:
        raise HTTPException(status_code=400, detail=f"Invalid stock symbol: {stock.symbol}")
    
    # Get current portfolio
    db = firestore.client()
    portfolio_ref = db.collection('portfolios').document(user_id)
    portfolio = portfolio_ref.get()
    
    current_stocks = []
    if portfolio.exists:
        current_stocks = portfolio.to_dict().get('stocks', [])
    
    # Check if stock already exists
    for i, existing_stock in enumerate(current_stocks):
        if existing_stock['symbol'] == stock.symbol:
            # Update existing stock
            current_stocks[i] = stock.dict()
            portfolio_ref.set({'stocks': current_stocks})
            return UserPortfolio(stocks=current_stocks)
    
    # Add new stock
    current_stocks.append(stock.dict())
    portfolio_ref.set({'stocks': current_stocks})
    
    return UserPortfolio(stocks=current_stocks)

@router.delete("/{symbol}", response_model=UserPortfolio)
async def remove_stock_from_portfolio(
    symbol: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Remove a stock from the portfolio"""
    user_id = await verify_firebase_token(credentials.credentials)
    
    # Get current portfolio
    db = firestore.client()
    portfolio_ref = db.collection('portfolios').document(user_id)
    portfolio = portfolio_ref.get()
    
    if not portfolio.exists:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    current_stocks = portfolio.to_dict().get('stocks', [])
    
    # Remove the stock
    updated_stocks = [stock for stock in current_stocks if stock['symbol'] != symbol]
    
    if len(updated_stocks) == len(current_stocks):
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found in portfolio")
    
    # Update in Firestore
    portfolio_ref.set({'stocks': updated_stocks})
    
    return UserPortfolio(stocks=updated_stocks)

@router.get("/performance", response_model=Dict)
async def get_portfolio_performance(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get the performance metrics for the user's portfolio"""
    user_id = await verify_firebase_token(credentials.credentials)
    
    # Get user portfolio
    db = firestore.client()
    portfolio_ref = db.collection('portfolios').document(user_id)
    portfolio = portfolio_ref.get()
    
    if not portfolio.exists or not portfolio.to_dict().get('stocks'):
        raise HTTPException(status_code=404, detail="Portfolio not found or empty")
    
    # Calculate portfolio metrics based on holdings
    # This would integrate the portfolio service
    # For now, return placeholder data
    
    return {
        "total_value": 10000.00,
        "daily_change": 1.2,  # percentage
        "total_return": 5.7,   # percentage
        "risk_level": "Moderate",
        "sector_allocation": {
            "Technology": 40,
            "Finance": 30,
            "Energy": 30
        }
    }