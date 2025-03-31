import yfinance as yf
import pandas as pd
from datetime import datetime
from typing import Dict

class StockService:
    @staticmethod
    async def get_stock_data(symbol: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Fetch historical stock data for a given symbol and date range."""
        try:
            stock = yf.Ticker(symbol)
            df = stock.history(start=start_date, end=end_date)
            
            if df.empty:
                raise ValueError(f"No data found for {symbol} in the specified date range")
                
            return df
        except Exception as e:
            raise ValueError(f"Error fetching stock data: {str(e)}")
    
    @staticmethod
    async def get_available_stocks() -> Dict[str, str]:
        """Return the dictionary of available Saudi stocks."""
        # In a real app, this might come from a database
        return {
            '2222.SR': 'Saudi Aramco - أرامكو السعودية',
            '1180.SR': 'Al Rajhi Bank - مصرف الراجحي',
            '2350.SR': 'Saudi Telecom Co - الاتصالات السعودية',
            '1010.SR': 'SABIC - سابك',
            '1150.SR': 'Alinma Bank - مصرف الإنماء',
            '2310.SR': 'Zain KSA - زين السعودية',
            '2380.SR': 'Mobily - موبايلي',
            '1050.SR': 'Saudi National Bank - البنك الأهلي السعودي',
            '2001.SR': 'ACWA Power - أكوا باور',
            '2330.SR': 'Advanced - المتقدمة'
        }