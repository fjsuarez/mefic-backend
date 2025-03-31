import yfinance as yf
from typing import Dict, Optional

class FinancialService:
    @staticmethod
    async def get_financial_metrics(symbol: str) -> Dict[str, Optional[float]]:
        """Get key financial metrics for a stock."""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # Extract metrics
            metrics = {
                "pe_ratio": info.get("trailingPE"),
                "roe": info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else None,
                "roa": info.get("returnOnAssets", 0) * 100 if info.get("returnOnAssets") else None,
                "dividend_yield": info.get("dividendYield", 0) * 100 if info.get("dividendYield") else None,
                "payout_ratio": info.get("payoutRatio", 0) * 100 if info.get("payoutRatio") else None,
            }
            
            # Calculate custom dividend score (simplified example)
            if metrics["dividend_yield"] and metrics["payout_ratio"]:
                # Simple scoring: higher yield and sustainable payout ratio (not too high) is better
                div_score = min(100, metrics["dividend_yield"] * 10)
                if metrics["payout_ratio"] > 80:
                    div_score *= 0.8  # Penalize very high payout ratios
                metrics["dividend_score"] = div_score
            else:
                metrics["dividend_score"] = None
                
            return metrics
        except Exception as e:
            raise ValueError(f"Error fetching financial metrics: {str(e)}")
    
    @staticmethod
    async def get_all_stocks_comparison(stock_dict: Dict[str, str]) -> list:
        """Get comparison metrics for all stocks in the provided dictionary."""
        result = []
        
        for symbol, company in stock_dict.items():
            try:
                metrics = await FinancialService.get_financial_metrics(symbol)
                result.append({
                    "symbol": symbol,
                    "company": company,
                    **metrics
                })
            except Exception:
                # If one stock fails, continue with others
                continue
                
        return result