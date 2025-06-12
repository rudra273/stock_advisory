# app/agents/technical_analysis_agent.py

from typing import Dict, Any, Optional
from datetime import datetime, date
from sqlalchemy.orm import Session

from app.agents.base import BaseAgent
from app.repositories.metrics_processor import MetricsProcessor, CalculatedMetrics
from app.services.llm.gemini_llm import GeminiLLM

class TechnicalAnalysisAgent(BaseAgent):
    """Technical analysis agent that provides comprehensive stock technical analysis"""
    
    def __init__(self, db: Session):
        self.db = db
        self.llm = GeminiLLM()
        self.llm_instance = self.llm.get_llm()
    
    def execute(self, symbol: str, **kwargs) -> Dict[str, Any]:
        """
        Execute technical analysis for a given stock symbol
        
        Args:
            symbol: Stock symbol to analyze
            
        Returns:
            Dictionary with comprehensive technical analysis
        """
        try:
            # Initialize processors
            metrics_processor = MetricsProcessor(self.db, symbol)
            calculated_metrics = CalculatedMetrics(metrics_processor)
            
            # Get all required data
            current_price_data = metrics_processor.get_current_price_metrics()
            stock_info = metrics_processor.get_stock_info_metrics()
            technical_data = calculated_metrics.get_comprehensive_technical_analysis()
            
            # Check if we have sufficient data
            if not current_price_data.get("current_price"):
                return self._create_error_response(symbol, "No current price data available")
            
            # Generate analysis
            analysis = self._generate_technical_analysis(
                symbol, current_price_data, stock_info, technical_data
            )
            
            return analysis
            
        except Exception as e:
            return self._create_error_response(symbol, str(e))
    
    def _generate_technical_analysis(self, symbol: str, price_data: Dict, 
                                   stock_info: Dict, technical_data: Dict) -> Dict[str, Any]:
        """Generate comprehensive technical analysis"""
        
        current_price = price_data.get("current_price")
        company_name = price_data.get("company_name", symbol)
        
        # A. Executive Summary
        executive_summary = self._generate_executive_summary(
            symbol, current_price, technical_data
        )
        
        # B. Narrative Analysis
        narrative_analysis = self._generate_narrative_analysis(
            current_price, technical_data
        )
        
        # C. Data Table
        data_table = self._generate_data_table(current_price, technical_data)
        
        return {
            "symbol": symbol,
            "company_name": company_name,
            "current_price": current_price,
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executive_summary": executive_summary,
            "narrative_analysis": narrative_analysis,
            "data_table": data_table,
            "raw_technical_data": technical_data
        }
    
    def _generate_executive_summary(self, symbol: str, current_price: float, 
                                  technical_data: Dict) -> Dict[str, Any]:
        """Generate executive summary with sentiment and key levels"""
        
        # Determine sentiment
        sentiment_score = self._calculate_sentiment_score(technical_data)
        sentiment = self._get_sentiment_label(sentiment_score)
        
        # Generate core thesis
        core_thesis = self._generate_core_thesis(symbol, current_price, technical_data, sentiment)
        
        # Get support/resistance levels
        support_resistance = technical_data.get("support_resistance", {})
        
        return {
            "sentiment": sentiment,
            "core_thesis": core_thesis,
            "key_levels": {
                "support": support_resistance.get("support"),
                "resistance": support_resistance.get("resistance"),
                "confidence": support_resistance.get("confidence", "Low")
            }
        }
    
    def _generate_narrative_analysis(self, current_price: float, 
                                   technical_data: Dict) -> Dict[str, Any]:
        """Generate detailed narrative analysis"""
        
        bullish_signals = self._identify_bullish_signals(current_price, technical_data)
        bearish_signals = self._identify_bearish_signals(current_price, technical_data)
        
        return {
            "bullish_signals": bullish_signals,
            "bearish_signals": bearish_signals
        }
    
    def _generate_data_table(self, current_price: float, technical_data: Dict) -> list:
        """Generate data table with metrics and interpretations"""
        
        ma_data = technical_data.get("moving_averages", {})
        rsi = technical_data.get("rsi")
        macd_data = technical_data.get("macd", {})
        atr = technical_data.get("atr")
        obv_data = technical_data.get("obv", {})
        
        table_data = []
        
        # Trend Analysis
        if ma_data.get("MA_50"):
            ma_50_interpretation = "Price is above (Bullish)" if current_price > ma_data["MA_50"] else "Price is below (Bearish)"
            table_data.append({
                "category": "Trend",
                "metric": "50-Day MA",
                "value": f"${ma_data['MA_50']:.2f}",
                "interpretation": ma_50_interpretation
            })
        
        if ma_data.get("MA_200"):
            ma_200_interpretation = "Price is above (Bullish)" if current_price > ma_data["MA_200"] else "Price is below (Bearish)"
            table_data.append({
                "category": "Trend",
                "metric": "200-Day MA",
                "value": f"${ma_data['MA_200']:.2f}",
                "interpretation": ma_200_interpretation
            })
        
        # Momentum Analysis
        if rsi:
            rsi_interpretation = self._interpret_rsi(rsi)
            table_data.append({
                "category": "Momentum",
                "metric": "RSI (14)",
                "value": f"{rsi:.1f}",
                "interpretation": rsi_interpretation
            })
        
        if macd_data.get("histogram"):
            macd_interpretation = "Rising Momentum" if macd_data["histogram"] > 0 else "Falling Momentum"
            table_data.append({
                "category": "Momentum",
                "metric": "MACD Histogram",
                "value": f"{macd_data['histogram']:+.2f}",
                "interpretation": macd_interpretation
            })
        
        # Volatility Analysis
        if atr:
            atr_interpretation = "Elevated Risk" if atr > 3 else "Moderate Risk" if atr > 1.5 else "Low Risk"
            table_data.append({
                "category": "Volatility",
                "metric": "ATR",
                "value": f"{atr:.1f}%",
                "interpretation": atr_interpretation
            })
        
        # Volume Analysis
        if obv_data.get("obv_trend"):
            obv_interpretation = "Confirms price move" if obv_data["obv_trend"] == "↑ trending" else "Diverges from price"
            table_data.append({
                "category": "Volume",
                "metric": "OBV",
                "value": obv_data["obv_trend"],
                "interpretation": obv_interpretation
            })
        
        return table_data
    
    def _calculate_sentiment_score(self, technical_data: Dict) -> float:
        """Calculate overall sentiment score from technical indicators"""
        score = 0
        indicators_count = 0
        
        # RSI scoring
        rsi = technical_data.get("rsi")
        if rsi:
            if rsi < 30:
                score += 1  # Oversold - bullish
            elif rsi > 70:
                score -= 1  # Overbought - bearish
            else:
                score += 0.5 if rsi < 50 else -0.5
            indicators_count += 1
        
        # MACD scoring
        macd_data = technical_data.get("macd", {})
        if macd_data.get("histogram"):
            score += 1 if macd_data["histogram"] > 0 else -1
            indicators_count += 1
        
        # Moving averages scoring
        ma_data = technical_data.get("moving_averages", {})
        if ma_data.get("MA_50") and ma_data.get("MA_200"):
            if ma_data["MA_50"] > ma_data["MA_200"]:
                score += 1  # Golden cross territory
            else:
                score -= 1  # Death cross territory
            indicators_count += 1
        
        # Stochastic scoring
        stochastic = technical_data.get("stochastic", {})
        if stochastic.get("percent_k"):
            if stochastic["percent_k"] < 20:
                score += 1  # Oversold
            elif stochastic["percent_k"] > 80:
                score -= 1  # Overbought
            indicators_count += 1
        
        # OBV scoring
        obv_data = technical_data.get("obv", {})
        if obv_data.get("obv_trend"):
            if obv_data["obv_trend"] == "↑ trending":
                score += 1
            elif obv_data["obv_trend"] == "↓ trending":
                score -= 1
            indicators_count += 1
        
        return score / indicators_count if indicators_count > 0 else 0
    
    def _get_sentiment_label(self, score: float) -> str:
        """Convert sentiment score to label"""
        if score > 0.3:
            return "Bullish"
        elif score < -0.3:
            return "Bearish"
        elif abs(score) <= 0.1:
            return "Neutral"
        else:
            return "Mixed Signals"
    
    def _generate_core_thesis(self, symbol: str, current_price: float, 
                            technical_data: Dict, sentiment: str) -> str:
        """Generate core thesis statement"""
        
        ma_data = technical_data.get("moving_averages", {})
        macd_data = technical_data.get("macd", {})
        obv_data = technical_data.get("obv", {})
        
        # Determine key trend signal
        if ma_data.get("MA_50") and current_price > ma_data["MA_50"]:
            trend_signal = f"breakout above its 50-day MA (${ma_data['MA_50']:.2f})"
        elif ma_data.get("MA_200") and current_price > ma_data["MA_200"]:
            trend_signal = f"holding above its 200-day MA (${ma_data['MA_200']:.2f})"
        elif macd_data.get("crossover_date"):
            trend_signal = f"MACD crossover on {macd_data['crossover_date']}"
        else:
            trend_signal = "mixed technical signals"
        
        # Volume confirmation
        volume_signal = ""
        if obv_data.get("obv_trend") == "↑ trending":
            volume_signal = " on rising volume"
        elif obv_data.get("obv_trend") == "↓ trending":
            volume_signal = " with declining volume"
        
        # Sentiment-based direction
        if sentiment == "Bullish":
            direction = "suggesting the start of a new uptrend"
        elif sentiment == "Bearish":
            direction = "indicating potential downside pressure"
        else:
            direction = "reflecting current market uncertainty"
        
        return f"${symbol} has shown {trend_signal}{volume_signal}, {direction}."
    
    def _identify_bullish_signals(self, current_price: float, technical_data: Dict) -> list:
        """Identify bullish technical signals"""
        signals = []
        
        # MACD signals
        macd_data = technical_data.get("macd", {})
        if macd_data.get("crossover_date") and macd_data.get("histogram", 0) > 0:
            signals.append(f"MACD Crossover: Occurred on {macd_data['crossover_date']}, indicating upward momentum.")
        
        # RSI signals
        rsi = technical_data.get("rsi")
        if rsi and rsi < 70:
            signals.append(f"RSI (14) = {rsi:.1f}: Below overbought threshold (<70), so room to run.")
        
        # Moving average signals
        ma_data = technical_data.get("moving_averages", {})
        ma_signals = []
        if ma_data.get("MA_50") and current_price > ma_data["MA_50"]:
            ma_signals.append(f"50-day MA (${ma_data['MA_50']:.2f})")
        if ma_data.get("MA_200") and current_price > ma_data["MA_200"]:
            ma_signals.append(f"200-day MA (${ma_data['MA_200']:.2f})")
        
        if ma_signals:
            signals.append(f"Price vs. Moving Averages: Current price above {' and '.join(ma_signals)}.")
        
        # Volume signals
        obv_data = technical_data.get("obv", {})
        if obv_data.get("obv_trend") == "↑ trending":
            signals.append("Volume Confirmation: On-Balance Volume trending upward, confirming price strength.")
        
        return signals if signals else ["No significant bullish signals identified."]
    
    def _identify_bearish_signals(self, current_price: float, technical_data: Dict) -> list:
        """Identify bearish technical signals"""
        signals = []
        
        # Stochastic signals
        stochastic = technical_data.get("stochastic", {})
        if stochastic.get("percent_k") and stochastic["percent_k"] > 80:
            signals.append(f"Stochastic Oscillator = {stochastic['percent_k']:.1f}: In overbought zone (>80), a possible pullback warning.")
        
        # Volatility signals
        atr = technical_data.get("atr")
        if atr and atr > 3:
            signals.append(f"Volatility (ATR) = {atr:.1f}%: Elevated volatility increases risk of whipsaws.")
        
        # RSI overbought
        rsi = technical_data.get("rsi")
        if rsi and rsi > 70:
            signals.append(f"RSI (14) = {rsi:.1f}: In overbought territory (>70), potential for correction.")
        
        # Moving average resistance
        ma_data = technical_data.get("moving_averages", {})
        if ma_data.get("MA_50") and current_price < ma_data["MA_50"]:
            signals.append(f"Price below 50-day MA (${ma_data['MA_50']:.2f}): Short-term downtrend.")
        
        # Volume divergence
        obv_data = technical_data.get("obv", {})
        if obv_data.get("obv_trend") == "↓ trending":
            signals.append("Volume Divergence: On-Balance Volume declining while price holding, potential weakness.")
        
        return signals if signals else ["No significant bearish signals identified."]
    
    def _interpret_rsi(self, rsi: float) -> str:
        """Interpret RSI value"""
        if rsi < 30:
            return "Oversold (Bullish)"
        elif rsi > 70:
            return "Overbought (Bearish)"
        elif rsi < 50:
            return "Moderate Momentum (Neutral-Bearish)"
        else:
            return "Moderate Momentum (Neutral-Bullish)"
    
    def _create_error_response(self, symbol: str, error_message: str) -> Dict[str, Any]:
        """Create error response when analysis fails"""
        return {
            "symbol": symbol,
            "error": True,
            "message": error_message,
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executive_summary": {
                "sentiment": "Insufficient Data",
                "core_thesis": f"Unable to perform technical analysis for {symbol}: {error_message}",
                "key_levels": {
                    "support": None,
                    "resistance": None,
                    "confidence": "Low"
                }
            },
            "narrative_analysis": {
                "bullish_signals": ["Insufficient data for analysis"],
                "bearish_signals": ["Insufficient data for analysis"]
            },
            "data_table": []
        }