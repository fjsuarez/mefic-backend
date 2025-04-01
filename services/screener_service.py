from typing import Dict, List
from services.financial_service import FinancialService
from services.stock_service import StockService

class ScreenerService:
    @staticmethod
    async def get_screener_data(weights: Dict[str, float] = None) -> List[Dict]:
        """
        Get screener data with weighted scores for all available stocks.
        
        Args:
            weights: Dictionary with weights for each metric 
                    (pe_ratio, roe, roa, dividend_yield)
        
        Returns:
            List of stocks with financial metrics and weighted score
        """
        # Default weights if none provided
        if weights is None:
            weights = {
                "pe_ratio": 0.25,
                "roe": 0.25,
                "roa": 0.25,
                "dividend_yield": 0.25
            }
            
        # Normalize weights to ensure they sum to 1.0
        total_weight = sum(weights.values())
        if total_weight != 0:
            normalized_weights = {k: v/total_weight for k, v in weights.items()}
        else:
            normalized_weights = weights
            
        # Get all available stocks
        stocks_dict = await StockService.get_available_stocks()
        
        # Get financial metrics for all stocks
        all_stocks_data = await FinancialService.get_all_stocks_comparison(stocks_dict)
        
        # Calculate weighted scores
        for stock in all_stocks_data:
            score = 0.0
            metrics_used = 0
            
            # PE Ratio (lower is better, so we invert it)
            if stock.get("pe_ratio") and normalized_weights.get("pe_ratio"):
                # Only use reasonable PE ratios (0-100)
                if 0 < stock["pe_ratio"] < 100:
                    # Normalize: lower PE ratio is better (1/PE)
                    score += (1/stock["pe_ratio"]) * normalized_weights["pe_ratio"] * 20
                    metrics_used += 1
            
            # ROE (higher is better)
            if stock.get("roe") and normalized_weights.get("roe"):
                # Normalize: 0-50% with 15% being average
                normalized_roe = min(stock["roe"] / 30, 1)
                score += normalized_roe * normalized_weights["roe"]
                metrics_used += 1
            
            # ROA (higher is better)
            if stock.get("roa") and normalized_weights.get("roa"):
                # Normalize: 0-20% with 6% being average
                normalized_roa = min(stock["roa"] / 12, 1)
                score += normalized_roa * normalized_weights["roa"]
                metrics_used += 1
            
            # Dividend Yield (higher is better)
            if stock.get("dividend_yield") and normalized_weights.get("dividend_yield"):
                # Normalize: 0-10% with 3.5% being average
                normalized_div = min(stock["dividend_yield"] / 7, 1)
                score += normalized_div * normalized_weights["dividend_yield"]
                metrics_used += 1
            
            # Adjust score if not all metrics available
            if metrics_used > 0:
                stock["weighted_score"] = (score / metrics_used) * 100
            else:
                stock["weighted_score"] = 0
                
        # Sort stocks by weighted score (descending)
        sorted_stocks = sorted(all_stocks_data, key=lambda x: x.get("weighted_score", 0), reverse=True)
        
        return sorted_stocks