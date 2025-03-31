import pandas as pd
import numpy as np
from typing import Dict

class TechnicalService:
    @staticmethod
    async def calculate_technical_indicators(df: pd.DataFrame) -> Dict[str, float]:
        """Calculate technical indicators for a given DataFrame of stock prices."""
        try:
            # Make a copy to avoid modifying the original DataFrame
            data = df.copy()
            
            # Calculate Simple Moving Averages
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            data['SMA_200'] = data['Close'].rolling(window=200).mean()
            
            # Calculate Exponential Moving Average
            data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
            
            # Calculate RSI
            delta = data['Close'].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(window=14).mean()
            avg_loss = loss.rolling(window=14).mean()
            rs = avg_gain / avg_loss
            data['RSI_14'] = 100 - (100 / (1 + rs))
            
            # Calculate MACD
            data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
            data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
            data['MACD'] = data['EMA_12'] - data['EMA_26']
            data['MACD_signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
            
            # Calculate Bollinger Bands
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['stddev'] = data['Close'].rolling(window=20).std()
            data['bollinger_upper'] = data['SMA_20'] + (data['stddev'] * 2)
            data['bollinger_lower'] = data['SMA_20'] - (data['stddev'] * 2)
            
            # Get the latest values
            latest = data.iloc[-1]
            
            return {
                "sma_20": latest['SMA_20'] if not np.isnan(latest['SMA_20']) else None,
                "sma_50": latest['SMA_50'] if not np.isnan(latest['SMA_50']) else None,
                "sma_200": latest['SMA_200'] if not np.isnan(latest['SMA_200']) else None,
                "ema_20": latest['EMA_20'] if not np.isnan(latest['EMA_20']) else None,
                "rsi_14": latest['RSI_14'] if not np.isnan(latest['RSI_14']) else None,
                "macd": latest['MACD'] if not np.isnan(latest['MACD']) else None,
                "macd_signal": latest['MACD_signal'] if not np.isnan(latest['MACD_signal']) else None,
                "bollinger_upper": latest['bollinger_upper'] if not np.isnan(latest['bollinger_upper']) else None,
                "bollinger_lower": latest['bollinger_lower'] if not np.isnan(latest['bollinger_lower']) else None
            }
        except Exception as e:
            raise ValueError(f"Error calculating technical indicators: {str(e)}")