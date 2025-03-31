import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict

class PortfolioService:
    @staticmethod
    async def calculate_portfolio_metrics(df: pd.DataFrame) -> Dict[str, float]:
        """Calculate portfolio metrics for a given DataFrame of stock prices."""
        try:
            # Calculate daily returns
            returns = df['Close'].pct_change().dropna()
            
            # Calculate annualized return
            annual_return = (1 + returns.mean()) ** 252 - 1
            
            # Get market data (Saudi index)
            market = yf.download('^TASI', 
                                start=df.index[0], 
                                end=df.index[-1])
            market_returns = market['Close'].pct_change().dropna()
            
            # Match the dates
            common_dates = returns.index.intersection(market_returns.index)
            stock_returns_aligned = returns.loc[common_dates]
            market_returns_aligned = market_returns.loc[common_dates]
            
            # Calculate beta
            covariance = stock_returns_aligned.cov(market_returns_aligned)
            market_variance = market_returns_aligned.var()
            beta = covariance / market_variance
            
            # Calculate Alpha
            risk_free_rate = 0.02 / 252  # Daily risk-free rate
            stock_annual_return = (1 + stock_returns_aligned.mean()) ** 252 - 1
            market_annual_return = (1 + market_returns_aligned.mean()) ** 252 - 1
            alpha = stock_annual_return - (risk_free_rate + beta * (market_annual_return - risk_free_rate))
            
            # Calculate Tracking Error
            tracking_diff = stock_returns_aligned - market_returns_aligned
            tracking_error = tracking_diff.std() * np.sqrt(252)
            
            # Calculate Information Ratio
            information_ratio = (stock_annual_return - market_annual_return) / tracking_error
            
            return {
                "annual_return": annual_return,
                "alpha": alpha,
                "info_ratio": information_ratio,
                "tracking_error": tracking_error
            }
        except Exception as e:
            raise ValueError(f"Error calculating portfolio metrics: {str(e)}")