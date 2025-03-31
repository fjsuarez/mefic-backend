import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict

class RiskService:
    @staticmethod
    async def calculate_risk_metrics(df: pd.DataFrame) -> Dict[str, float]:
        """Calculate risk metrics for a given DataFrame of stock prices."""
        try:
            # Calculate daily returns
            returns = df['Close'].pct_change().dropna()
            
            # Calculate volatility (annualized)
            volatility = returns.std() * np.sqrt(252)
            
            try:
                # Try to get the market returns (TASI - Saudi index)
                market = yf.download('^TASI', 
                                    start=df.index[0], 
                                    end=df.index[-1])
                
                if not market.empty:
                    market_returns = market['Close'].pct_change().dropna()
                    
                    # Match the dates
                    common_dates = returns.index.intersection(market_returns.index)
                    stock_returns_aligned = returns.loc[common_dates]
                    market_returns_aligned = market_returns.loc[common_dates]
                    
                    # Calculate beta
                    covariance = stock_returns_aligned.cov(market_returns_aligned)
                    market_variance = market_returns_aligned.var()
                    beta = covariance / market_variance
                else:
                    # Fallback if market data is empty
                    beta = 1.0  # Neutral beta as fallback
            except Exception:
                # Fallback if market data fails to download
                beta = 1.0  # Neutral beta as fallback
            
            # Calculate Sharpe Ratio (assuming risk-free rate of 0.02 or 2%)
            risk_free_rate = 0.02 / 252  # Daily risk-free rate
            sharpe_ratio = (returns.mean() - risk_free_rate) / returns.std() * np.sqrt(252)
            
            # Calculate Max Drawdown
            cumulative_returns = (1 + returns).cumprod()
            max_return = cumulative_returns.cummax()
            drawdown = (cumulative_returns / max_return) - 1
            max_drawdown = drawdown.min()
            
            return {
                "beta": beta,
                "volatility": volatility,
                "sharpe_ratio": sharpe_ratio,
                "max_drawdown": max_drawdown
            }
        except Exception as e:
            raise ValueError(f"Error calculating risk metrics: {str(e)}")