# from typing import Dict, Any, Optional
# from datetime import datetime, date
# from sqlalchemy.orm import Session

# from app.agents.base import BaseAgent
# from app.repositories.metrics_processor import MetricsProcessor, CalculatedMetrics
# from app.services.llm.gemini_llm import GeminiLLM

# class TechnicalAnalysisAgent(BaseAgent):
#     """Technical analysis agent that provides comprehensive stock technical analysis"""
#     def __init__(self, db: Session):
#         self.db = db
#         self.llm = GeminiLLM()
#         self.llm_instance = self.llm.get_llm()

#     def execute(self, symbol: str, **kwargs) -> Dict[str, Any]:
#         """Execute technical analysis for a given stock symbol"""
#         try:
#             metrics_processor = MetricsProcessor(self.db, symbol)
#             calculated_metrics = CalculatedMetrics(metrics_processor)
#             current_price_data = metrics_processor.get_current_price_metrics()
#             stock_info = metrics_processor.get_stock_info_metrics()
#             technical_data = calculated_metrics.get_comprehensive_technical_analysis()
#             if not current_price_data.get("current_price"):
#                 return self._create_error_response(symbol, "No current price data available")
#             analysis = self._generate_technical_analysis(
#                 symbol, current_price_data, stock_info, technical_data
#             )
#             return analysis
#         except Exception as e:
#             return self._create_error_response(symbol, str(e))

#     def _generate_technical_analysis(self, symbol: str, price_data: Dict, 
#                                    stock_info: Dict, technical_data: Dict) -> Dict[str, Any]:
#         """Generate comprehensive technical analysis"""
#         current_price = price_data.get("current_price")
#         company_name = price_data.get("company_name", symbol)
        
#         # Generate LLM-enhanced analysis
#         executive_summary = self._generate_executive_summary(
#             symbol, current_price, technical_data
#         )
#         narrative_analysis = self._generate_llm_narrative_analysis(
#             symbol, current_price, technical_data
#         )
#         data_table = self._generate_data_table(current_price, technical_data)
        
#         return {
#             "symbol": symbol,
#             "company_name": company_name,
#             "current_price": current_price,
#             "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "executive_summary": executive_summary,
#             "llm_generated_narrative_analysis": narrative_analysis,
#             "data_table": data_table,
#             "raw_technical_data": technical_data
#         }

#     def _generate_executive_summary(self, symbol: str, current_price: float, 
#                                   technical_data: Dict) -> Dict[str, Any]:
#         """Generate executive summary with LLM-generated thesis"""
#         sentiment_score = self._calculate_sentiment_score(technical_data)
#         sentiment = self._get_sentiment_label(sentiment_score)
        
#         # Generate LLM thesis
#         llm_thesis = self._generate_llm_thesis(symbol, current_price, technical_data, sentiment)
        
#         support_resistance = technical_data.get("support_resistance", {})
#         return {
#             "overall_sentiment": sentiment,
#             "llm_generated_thesis": llm_thesis,
#             "key_levels": {
#                 "support": support_resistance.get("support"),
#                 "resistance": support_resistance.get("resistance"),
#                 "confidence": support_resistance.get("confidence", "Low")
#             }
#         }

#     def _generate_llm_thesis(self, symbol: str, current_price: float, 
#                            technical_data: Dict, sentiment: str) -> str:
#         """Generate LLM-powered executive thesis"""
#         try:
#             print(f"Generating LLM thesis for {symbol} at price ₹{current_price:.2f} with sentiment '{sentiment}'")
#             # Prepare comprehensive technical context
#             context = self._prepare_technical_context(symbol, current_price, technical_data, sentiment)
            
#             prompt = f"""You are an expert technical analyst. Based on the following technical data for {symbol}, 
# generate a concise, professional executive thesis (2-3 sentences) that synthesizes the key technical outlook.

# Technical Context:
# {context}

# Requirements:
# - Synthesize the most significant technical indicators into a coherent narrative
# - Explain the implications of the current price position relative to key levels
# - Address any notable divergences or confirmations between indicators
# - Keep it concise but comprehensive
# - Use professional financial languag


# Generate only the thesis statement, no additional commentary."""

#             response = self.llm_instance.invoke(prompt)
#             return response.content.strip() 
        
#         except Exception as e:
#             print(f"LLM thesis generation failed: {e}")
#             # Fallback to rule-based thesis if LLM fails
#             return self._generate_core_thesis(symbol, current_price, technical_data, sentiment)

#     def _generate_llm_narrative_analysis(self, symbol: str, current_price: float, 
#                                        technical_data: Dict) -> Dict[str, Any]:
#         """Generate comprehensive LLM-powered narrative analysis"""
#         try:
#             # Prepare technical context
#             context = self._prepare_technical_context(symbol, current_price, technical_data)
            
#             # Generate summary
#             summary_prompt = f"""As a technical analyst, provide a comprehensive summary of the current technical picture for {symbol}.

# {context}

# Generate a detailed summary (2-3 sentences) that:
# - Describes the overall technical environment
# - Highlights key trend indicators and their implications
# - Addresses momentum and volume characteristics
# - Mentions any notable technical patterns or divergences
# - Concludes with the general market outlook for the stock


# Provide only the summary, no additional sections."""

#             summary_response = self.llm_instance.invoke(summary_prompt)
#             summary = summary_response.content.strip() 

            
#             # Generate bullish outlook

#             bullish_prompt = f"""Analyze the technical data for {symbol} and provide a bullish outlook in 100-120 words.

#             {context}

#             Requirements:
#             - Write ONLY 2-3 complete sentences
#             - Start directly with technical analysis, no introductory phrases
#             - Focus on: positive indicators, supportive price action, upside catalysts, risk/reward
#             - Use professional, direct tone
#             - No conversational language like "let's break down" or "here's a detailed"
#             - Use ₹ (rupee symbol) for all price references, not ₹ (dollar sign)

#             Format: Start immediately with your analysis."""


#             bullish_response = self.llm_instance.invoke(bullish_prompt)
#             bullish_outlook = bullish_response.content.strip() 

            
#             # Generate bearish outlook
#             bearish_prompt = f"""Analyze the technical data for {symbol} and provide a bearish outlook in 100-120 words.

#             {context}

#             Requirements:
#             - Write ONLY 2-3 complete sentences  
#             - Start directly with technical analysis, no introductory phrases
#             - Focus on: concerning indicators, negative price action, downside risks, key levels
#             - Use professional, direct tone
#             - No conversational language like "let's break down" or "here's a detailed"

#             Format: Start immediately with your analysis."""

#             bearish_response = self.llm_instance.invoke(bearish_prompt)
#             bearish_outlook = bearish_response.content.strip()
            
#             return {
#                 "summary": summary,
#                 "bullish_outlook": bullish_outlook,
#                 "bearish_outlook": bearish_outlook
#             }
            
#         except Exception as e:
#             print(f"LLM narrative analysis failed: {e}") 
#             # Fallback to rule-based analysis if LLM fails
#             return self._generate_narrative_analysis(current_price, technical_data)

#     def _prepare_technical_context(self, symbol: str, current_price: float, 
#                                  technical_data: Dict, sentiment: str = None) -> str:
#         """Prepare comprehensive technical context for LLM prompts"""
#         ma_data = technical_data.get("moving_averages", {})
#         rsi = technical_data.get("rsi")
#         macd_data = technical_data.get("macd", {})
#         stochastic = technical_data.get("stochastic", {})
#         atr = technical_data.get("atr")
#         obv_data = technical_data.get("obv", {})
#         support_resistance = technical_data.get("support_resistance", {})
        
#         context_parts = [
#             f"Symbol: {symbol}",
#             f"Current Price: ₹{current_price:.2f}"
#         ]
        
#         if sentiment:
#             context_parts.append(f"Overall Sentiment: {sentiment}")
        
#         # Moving Averages
#         if ma_data.get("MA_50"):
#             ma_50_status = "above" if current_price > ma_data["MA_50"] else "below"
#             context_parts.append(f"50-day MA: ₹{ma_data['MA_50']:.2f} (Price is {ma_50_status})")
            
#         if ma_data.get("MA_200"):
#             ma_200_status = "above" if current_price > ma_data["MA_200"] else "below"
#             context_parts.append(f"200-day MA: ₹{ma_data['MA_200']:.2f} (Price is {ma_200_status})")
        
#         # RSI
#         if rsi:
#             rsi_status = "Oversold" if rsi < 30 else "Overbought" if rsi > 70 else "Neutral"
#             context_parts.append(f"RSI (14): {rsi:.1f} ({rsi_status})")
        
#         # MACD
#         if macd_data.get("histogram") is not None:
#             macd_trend = "Positive" if macd_data["histogram"] > 0 else "Negative"
#             context_parts.append(f"MACD Histogram: {macd_data['histogram']:+.3f} ({macd_trend} momentum)")
            
#         if macd_data.get("crossover_date"):
#             context_parts.append(f"MACD Crossover: {macd_data['crossover_date']}")
        
#         # Stochastic
#         if stochastic.get("percent_k"):
#             stoch_status = "Oversold" if stochastic["percent_k"] < 20 else "Overbought" if stochastic["percent_k"] > 80 else "Neutral"
#             context_parts.append(f"Stochastic %K: {stochastic['percent_k']:.1f} ({stoch_status})")
        
#         # Volume (OBV)
#         if obv_data.get("obv_trend"):
#             context_parts.append(f"On-Balance Volume: {obv_data['obv_trend']}")
        
#         # Volatility
#         if atr:
#             vol_level = "High" if atr > 3 else "Moderate" if atr > 1.5 else "Low"
#             context_parts.append(f"Average True Range: {atr:.1f}% ({vol_level} volatility)")
        
#         # Support/Resistance
#         if support_resistance.get("support") and support_resistance.get("resistance"):
#             context_parts.append(f"Key Support: ₹{support_resistance['support']:.2f}")
#             context_parts.append(f"Key Resistance: ₹{support_resistance['resistance']:.2f}")
#             context_parts.append(f"Support/Resistance Confidence: {support_resistance.get('confidence', 'Unknown')}")
        
#         return "\n".join(context_parts)

#     def _generate_narrative_analysis(self, current_price: float, 
#                                    technical_data: Dict) -> Dict[str, Any]:
#         """Generate detailed narrative analysis (fallback method)"""
#         bullish_signals = self._identify_bullish_signals(current_price, technical_data)
#         bearish_signals = self._identify_bearish_signals(current_price, technical_data)
        
#         # Create a basic summary for fallback
#         summary = "Technical analysis shows mixed signals with both bullish and bearish indicators present. Key levels should be monitored for directional confirmation."
        
#         return {
#             "summary": summary,
#             "bullish_outlook": " ".join(bullish_signals),
#             "bearish_outlook": " ".join(bearish_signals)
#         }

#     def _generate_data_table(self, current_price: float, technical_data: Dict) -> list:
#         """Generate data table with metrics and interpretations"""
#         ma_data = technical_data.get("moving_averages", {})
#         rsi = technical_data.get("rsi")
#         macd_data = technical_data.get("macd", {})
#         atr = technical_data.get("atr")
#         obv_data = technical_data.get("obv", {})
#         table_data = []
#         if ma_data.get("MA_50"):
#             ma_50_interpretation = "Price is above (Bullish)" if current_price > ma_data["MA_50"] else "Price is below (Bearish)"
#             table_data.append({
#                 "category": "Trend",
#                 "metric": "50-Day MA",
#                 "value": f"₹{ma_data['MA_50']:.2f}",
#                 "interpretation": ma_50_interpretation
#             })
#         if ma_data.get("MA_200"):
#             ma_200_interpretation = "Price is above (Bullish)" if current_price > ma_data["MA_200"] else "Price is below (Bearish)"
#             table_data.append({
#                 "category": "Trend",
#                 "metric": "200-Day MA",
#                 "value": f"₹{ma_data['MA_200']:.2f}",
#                 "interpretation": ma_200_interpretation
#             })
#         if rsi:
#             rsi_interpretation = self._interpret_rsi(rsi)
#             table_data.append({
#                 "category": "Momentum",
#                 "metric": "RSI (14)",
#                 "value": f"{rsi:.1f}",
#                 "interpretation": rsi_interpretation
#             })
#         if macd_data.get("histogram"):
#             macd_interpretation = "Rising Momentum" if macd_data["histogram"] > 0 else "Falling Momentum"
#             table_data.append({
#                 "category": "Momentum",
#                 "metric": "MACD Histogram",
#                 "value": f"{macd_data['histogram']:+.2f}",
#                 "interpretation": macd_interpretation
#             })
#         if atr:
#             atr_interpretation = "Elevated Risk" if atr > 3 else "Moderate Risk" if atr > 1.5 else "Low Risk"
#             table_data.append({
#                 "category": "Volatility",
#                 "metric": "ATR",
#                 "value": f"{atr:.1f}%",
#                 "interpretation": atr_interpretation
#             })
#         if obv_data.get("obv_trend"):
#             obv_interpretation = "Confirms price move" if obv_data["obv_trend"] == "↑ trending" else "Diverges from price"
#             table_data.append({
#                 "category": "Volume",
#                 "metric": "OBV",
#                 "value": obv_data["obv_trend"],
#                 "interpretation": obv_interpretation
#             })
#         return table_data

#     def _calculate_sentiment_score(self, technical_data: Dict) -> float:
#         """Calculate overall sentiment score from technical indicators"""
#         score = 0
#         indicators_count = 0
#         rsi = technical_data.get("rsi")
#         if rsi:
#             if rsi < 30:
#                 score += 1
#             elif rsi > 70:
#                 score -= 1
#             else:
#                 score += 0.5 if rsi < 50 else -0.5
#             indicators_count += 1
#         macd_data = technical_data.get("macd", {})
#         if macd_data.get("histogram"):
#             score += 1 if macd_data["histogram"] > 0 else -1
#             indicators_count += 1
#         ma_data = technical_data.get("moving_averages", {})
#         if ma_data.get("MA_50") and ma_data.get("MA_200"):
#             if ma_data["MA_50"] > ma_data["MA_200"]:
#                 score += 1
#             else:
#                 score -= 1
#             indicators_count += 1
#         stochastic = technical_data.get("stochastic", {})
#         if stochastic.get("percent_k"):
#             if stochastic["percent_k"] < 20:
#                 score += 1
#             elif stochastic["percent_k"] > 80:
#                 score -= 1
#             indicators_count += 1
#         obv_data = technical_data.get("obv", {})
#         if obv_data.get("obv_trend"):
#             if obv_data["obv_trend"] == "↑ trending":
#                 score += 1
#             elif obv_data["obv_trend"] == "↓ trending":
#                 score -= 1
#             indicators_count += 1
#         return score / indicators_count if indicators_count > 0 else 0

#     def _get_sentiment_label(self, score: float) -> str:
#         """Convert sentiment score to label"""
#         if score > 0.3:
#             return "Bullish"
#         elif score < -0.3:
#             return "Bearish"
#         elif abs(score) <= 0.1:
#             return "Neutral"
#         else:
#             return "Mixed Signals"

#     def _generate_core_thesis(self, symbol: str, current_price: float, 
#                             technical_data: Dict, sentiment: str) -> str:
#         """Generate core thesis statement (fallback method)"""
#         ma_data = technical_data.get("moving_averages", {})
#         macd_data = technical_data.get("macd", {})
#         obv_data = technical_data.get("obv", {})
#         if ma_data.get("MA_50") and current_price > ma_data["MA_50"]:
#             trend_signal = f"breakout above its 50-day MA (₹{ma_data['MA_50']:.2f})"
#         elif ma_data.get("MA_200") and current_price > ma_data["MA_200"]:
#             trend_signal = f"holding above its 200-day MA (₹{ma_data['MA_200']:.2f})"
#         elif macd_data.get("crossover_date"):
#             trend_signal = f"MACD crossover on {macd_data['crossover_date']}"
#         else:
#             trend_signal = "mixed technical signals"
#         volume_signal = ""
#         if obv_data.get("obv_trend") == "↑ trending":
#             volume_signal = " on rising volume"
#         elif obv_data.get("obv_trend") == "↓ trending":
#             volume_signal = " with declining volume"
#         if sentiment == "Bullish":
#             direction = "suggesting the start of a new uptrend"
#         elif sentiment == "Bearish":
#             direction = "indicating potential downside pressure"
#         else:
#             direction = "reflecting current market uncertainty"
#         return f"{symbol} has shown {trend_signal}{volume_signal}, {direction}."

#     def _identify_bullish_signals(self, current_price: float, technical_data: Dict) -> list:
#         """Identify bullish technical signals"""
#         signals = []
#         macd_data = technical_data.get("macd", {})
#         if macd_data.get("crossover_date") and macd_data.get("histogram", 0) > 0:
#             signals.append(f"MACD Crossover: Occurred on {macd_data['crossover_date']}, indicating upward momentum.")
#         rsi = technical_data.get("rsi")
#         if rsi and rsi < 70:
#             signals.append(f"RSI (14) = {rsi:.1f}: Below overbought threshold (<70), so room to run.")
#         ma_data = technical_data.get("moving_averages", {})
#         ma_signals = []
#         if ma_data.get("MA_50") and current_price > ma_data["MA_50"]:
#             ma_signals.append(f"50-day MA (₹{ma_data['MA_50']:.2f})")
#         if ma_data.get("MA_200") and current_price > ma_data["MA_200"]:
#             ma_signals.append(f"200-day MA (₹{ma_data['MA_200']:.2f})")
#         if ma_signals:
#             signals.append(f"Price vs. Moving Averages: Current price above {' and '.join(ma_signals)}.")
#         obv_data = technical_data.get("obv", {})
#         if obv_data.get("obv_trend") == "↑ trending":
#             signals.append("Volume Confirmation: On-Balance Volume trending upward, confirming price strength.")
#         return signals if signals else ["No significant bullish signals identified."]

#     def _identify_bearish_signals(self, current_price: float, technical_data: Dict) -> list:
#         """Identify bearish technical signals"""
#         signals = []
#         stochastic = technical_data.get("stochastic", {})
#         if stochastic.get("percent_k") and stochastic["percent_k"] > 80:
#             signals.append(f"Stochastic Oscillator = {stochastic['percent_k']:.1f}: In overbought zone (>80), a possible pullback warning.")
#         atr = technical_data.get("atr")
#         if atr and atr > 3:
#             signals.append(f"Volatility (ATR) = {atr:.1f}%: Elevated volatility increases risk of whipsaws.")
#         rsi = technical_data.get("rsi")
#         if rsi and rsi > 70:
#             signals.append(f"RSI (14) = {rsi:.1f}: In overbought territory (>70), potential for correction.")
#         ma_data = technical_data.get("moving_averages", {})
#         if ma_data.get("MA_50") and current_price < ma_data["MA_50"]:
#             signals.append(f"Price below 50-day MA (₹{ma_data['MA_50']:.2f}): Short-term downtrend.")
#         obv_data = technical_data.get("obv", {})
#         if obv_data.get("obv_trend") == "↓ trending":
#             signals.append("Volume Divergence: On-Balance Volume declining while price holding, potential weakness.")
#         return signals if signals else ["No significant bearish signals identified."]

#     def _interpret_rsi(self, rsi: float) -> str:
#         """Interpret RSI value"""
#         if rsi < 30:
#             return "Oversold (Bullish)"
#         elif rsi > 70:
#             return "Overbought (Bearish)"
#         elif rsi < 50:
#             return "Moderate Momentum (Neutral-Bearish)"
#         else:
#             return "Moderate Momentum (Neutral-Bullish)"

#     def _create_error_response(self, symbol: str, error_message: str) -> Dict[str, Any]:
#         """Create error response when analysis fails"""
#         return {
#             "symbol": symbol,
#             "error": True,
#             "message": error_message,
#             "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "executive_summary": {
#                 "overall_sentiment": "Insufficient Data",
#                 "llm_generated_thesis": f"Unable to perform technical analysis for {symbol}: {error_message}",
#                 "key_levels": {
#                     "support": None,
#                     "resistance": None,
#                     "confidence": "Low"
#                 }
#             },
#             "llm_generated_narrative_analysis": {
#                 "summary": "Insufficient data for analysis",
#                 "bullish_outlook": "Insufficient data for analysis",
#                 "bearish_outlook": "Insufficient data for analysis"
#             },
#             "data_table": []
#         }


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
        """Execute technical analysis for a given stock symbol"""
        try:
            metrics_processor = MetricsProcessor(self.db, symbol)
            calculated_metrics = CalculatedMetrics(metrics_processor)
            current_price_data = metrics_processor.get_current_price_metrics()
            stock_info = metrics_processor.get_stock_info_metrics()
            technical_data = calculated_metrics.get_comprehensive_technical_analysis()
            if not current_price_data.get("current_price"):
                return self._create_error_response(symbol, "No current price data available")
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
        
        # Generate LLM-enhanced analysis
        executive_summary = self._generate_executive_summary(
            symbol, current_price, technical_data
        )
        narrative_analysis = self._generate_llm_narrative_analysis(
            symbol, current_price, technical_data
        )
        data_table = self._generate_data_table(current_price, technical_data)
        
        return {
            "symbol": symbol,
            "company_name": company_name,
            "current_price": current_price,
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executive_summary": executive_summary,
            "llm_generated_narrative_analysis": narrative_analysis,
            "data_table": data_table,
            "raw_technical_data": technical_data
        }

    def _generate_executive_summary(self, symbol: str, current_price: float, 
                                    technical_data: Dict) -> Dict[str, Any]:
        """Generate executive summary with LLM-generated thesis"""
        sentiment_score = self._calculate_sentiment_score(current_price, technical_data) # FIXED: Pass current_price
        sentiment = self._get_sentiment_label(sentiment_score)
        
        # Generate LLM thesis
        llm_thesis = self._generate_llm_thesis(symbol, current_price, technical_data, sentiment)
        
        support_resistance = technical_data.get("support_resistance", {})
        return {
            "overall_sentiment": sentiment,
            "llm_generated_thesis": llm_thesis,
            "key_levels": {
                "support": support_resistance.get("support"),
                "resistance": support_resistance.get("resistance"),
                "confidence": support_resistance.get("confidence", "Low")
            }
        }

    def _generate_llm_thesis(self, symbol: str, current_price: float, 
                             technical_data: Dict, sentiment: str) -> str:
        """Generate LLM-powered executive thesis"""
        try:
            print(f"Generating LLM thesis for {symbol} at price ₹{current_price:.2f} with sentiment '{sentiment}'")
            # Prepare comprehensive technical context
            context = self._prepare_technical_context(symbol, current_price, technical_data, sentiment)
            
            prompt = f"""You are an expert technical analyst. Based on the following technical data for {symbol}, 
generate a concise, professional executive thesis (2-3 sentences) that synthesizes the key technical outlook.

Technical Context:
{context}

Requirements:
- Synthesize the most significant technical indicators into a coherent narrative.
- Explain the implications of the current price position relative to key levels.
- Address any notable divergences or confirmations between indicators.
- Be concise but comprehensive.
- Use professional financial language.
- Use ₹ (rupee symbol) for all price references.

Generate only the thesis statement, no additional commentary."""

            response = self.llm_instance.invoke(prompt)
            return response.content.strip() 
        
        except Exception as e:
            print(f"LLM thesis generation failed: {e}")
            # Fallback to rule-based thesis if LLM fails
            return self._generate_core_thesis(symbol, current_price, technical_data, sentiment)

    def _generate_llm_narrative_analysis(self, symbol: str, current_price: float, 
                                         technical_data: Dict) -> Dict[str, Any]:
        """Generate comprehensive LLM-powered narrative analysis"""
        try:
            # Prepare technical context
            context = self._prepare_technical_context(symbol, current_price, technical_data)
            
            # Generate summary
            summary_prompt = f"""As a technical analyst, provide a comprehensive summary of the current technical picture for {symbol}.

{context}

Generate a detailed summary (2-3 sentences) that:
- Describes the overall technical environment.
- Highlights key trend indicators and their implications.
- Addresses momentum and volume characteristics.
- Mentions any notable technical patterns or divergences.
- Concludes with the general market outlook for the stock.
- Use ₹ (rupee symbol) for all price references.

Provide only the summary, no additional sections."""

            summary_response = self.llm_instance.invoke(summary_prompt)
            summary = summary_response.content.strip() 

            # CHANGED: Made word count constraint more flexible for better LLM performance
            bullish_prompt = f"""Analyze the technical data for {symbol} and provide a bullish outlook in approximately 100 words.

{context}

Requirements:
- Write 2-3 complete sentences.
- Start directly with technical analysis, no introductory phrases.
- Focus on: positive indicators, supportive price action, upside catalysts, risk/reward.
- Use professional, direct tone.
- No conversational language like "let's break down" or "here's a detailed".
- Use ₹ (rupee symbol) for all price references.

Format: Start immediately with your analysis."""

            bullish_response = self.llm_instance.invoke(bullish_prompt)
            bullish_outlook = bullish_response.content.strip() 
            
            # CHANGED: Made word count constraint more flexible for better LLM performance
            bearish_prompt = f"""Analyze the technical data for {symbol} and provide a bearish outlook in approximately 100 words.

{context}

Requirements:
- Write 2-3 complete sentences. 
- Start directly with technical analysis, no introductory phrases.
- Focus on: concerning indicators, negative price action, downside risks, key levels.
- Use professional, direct tone.
- No conversational language like "let's break down" or "here's a detailed".
- Use ₹ (rupee symbol) for all price references.

Format: Start immediately with your analysis."""

            bearish_response = self.llm_instance.invoke(bearish_prompt)
            bearish_outlook = bearish_response.content.strip()
            
            return {
                "summary": summary,
                "bullish_outlook": bullish_outlook,
                "bearish_outlook": bearish_outlook
            }
            
        except Exception as e:
            print(f"LLM narrative analysis failed: {e}") 
            # Fallback to rule-based analysis if LLM fails
            return self._generate_narrative_analysis(current_price, technical_data)

    def _prepare_technical_context(self, symbol: str, current_price: float, 
                                   technical_data: Dict, sentiment: str = None) -> str:
        """Prepare comprehensive technical context for LLM prompts"""
        ma_data = technical_data.get("moving_averages", {})
        rsi = technical_data.get("rsi")
        macd_data = technical_data.get("macd", {})
        stochastic = technical_data.get("stochastic", {})
        atr = technical_data.get("atr")
        obv_data = technical_data.get("obv", {})
        support_resistance = technical_data.get("support_resistance", {})
        
        context_parts = [
            f"Symbol: {symbol}",
            f"Current Price: ₹{current_price:.2f}"  # FIXED: Changed $ to ₹
        ]
        
        if sentiment:
            context_parts.append(f"Overall Sentiment: {sentiment}")
        
        # Moving Averages
        if ma_data.get("MA_50"):
            ma_50_status = "above" if current_price > ma_data["MA_50"] else "below"
            context_parts.append(f"50-day MA: ₹{ma_data['MA_50']:.2f} (Price is {ma_50_status})") # FIXED: Changed $ to ₹
            
        if ma_data.get("MA_200"):
            ma_200_status = "above" if current_price > ma_data["MA_200"] else "below"
            context_parts.append(f"200-day MA: ₹{ma_data['MA_200']:.2f} (Price is {ma_200_status})") # FIXED: Changed $ to ₹
        
        # RSI
        if rsi:
            rsi_status = "Oversold (<30)" if rsi < 30 else "Overbought (>70)" if rsi > 70 else "Neutral"
            context_parts.append(f"RSI (14): {rsi:.1f} ({rsi_status})")
        
        # MACD
        if macd_data.get("histogram") is not None:
            macd_trend = "Positive" if macd_data["histogram"] > 0 else "Negative"
            context_parts.append(f"MACD Histogram: {macd_data['histogram']:+.3f} ({macd_trend} momentum)")
            
        if macd_data.get("crossover_date"):
            context_parts.append(f"MACD Crossover: {macd_data['crossover_date']}")
        
        # Stochastic
        if stochastic.get("percent_k"):
            stoch_status = "Oversold (<20)" if stochastic["percent_k"] < 20 else "Overbought (>80)" if stochastic["percent_k"] > 80 else "Neutral"
            context_parts.append(f"Stochastic %K: {stochastic['percent_k']:.1f} ({stoch_status})")
        
        # Volume (OBV)
        if obv_data.get("obv_trend"):
            context_parts.append(f"On-Balance Volume: {obv_data['obv_trend']}")
        
        # Volatility
        if atr:
            vol_level = "High" if atr > 3 else "Moderate" if atr > 1.5 else "Low"
            context_parts.append(f"Average True Range: {atr:.1f}% ({vol_level} volatility)")
        
        # Support/Resistance
        if support_resistance.get("support") and support_resistance.get("resistance"):
            context_parts.append(f"Key Support: ₹{support_resistance['support']:.2f}") # FIXED: Changed $ to ₹
            context_parts.append(f"Key Resistance: ₹{support_resistance['resistance']:.2f}") # FIXED: Changed $ to ₹
            context_parts.append(f"Support/Resistance Confidence: {support_resistance.get('confidence', 'Unknown')}")
        
        return "\n".join(context_parts)

    def _generate_narrative_analysis(self, current_price: float, 
                                     technical_data: Dict) -> Dict[str, Any]:
        """Generate detailed narrative analysis (fallback method)"""
        bullish_signals = self._identify_bullish_signals(current_price, technical_data)
        bearish_signals = self._identify_bearish_signals(current_price, technical_data)
        
        # Create a basic summary for fallback
        summary = "Technical analysis shows mixed signals with both bullish and bearish indicators present. Key levels should be monitored for directional confirmation."
        
        return {
            "summary": summary,
            "bullish_outlook": " ".join(bullish_signals),
            "bearish_outlook": " ".join(bearish_signals)
        }

    def _generate_data_table(self, current_price: float, technical_data: Dict) -> list:
        """Generate data table with metrics and interpretations"""
        ma_data = technical_data.get("moving_averages", {})
        rsi = technical_data.get("rsi")
        macd_data = technical_data.get("macd", {})
        atr = technical_data.get("atr")
        obv_data = technical_data.get("obv", {})
        table_data = []

        # Trend
        if ma_data.get("MA_50"):
            table_data.append({
                "category": "Trend",
                "metric": "50-Day MA",
                "value": f"₹{ma_data['MA_50']:.2f}", # FIXED: Changed $ to ₹
                "interpretation": "Price is above (Bullish)" if current_price > ma_data["MA_50"] else "Price is below (Bearish)"
            })
        if ma_data.get("MA_200"):
            table_data.append({
                "category": "Trend",
                "metric": "200-Day MA",
                "value": f"₹{ma_data['MA_200']:.2f}", # FIXED: Changed $ to ₹
                "interpretation": "Price is above (Bullish)" if current_price > ma_data["MA_200"] else "Price is below (Bearish)"
            })

        # Momentum
        if rsi:
            table_data.append({
                "category": "Momentum",
                "metric": "RSI (14)",
                "value": f"{rsi:.1f}",
                "interpretation": self._interpret_rsi(rsi)
            })
        if macd_data.get("histogram"):
            table_data.append({
                "category": "Momentum",
                "metric": "MACD Histogram",
                "value": f"{macd_data['histogram']:+.2f}",
                "interpretation": "Rising Momentum" if macd_data["histogram"] > 0 else "Falling Momentum"
            })

        # Volatility
        if atr:
            table_data.append({
                "category": "Volatility",
                "metric": "ATR",
                "value": f"{atr:.1f}%",
                "interpretation": "Elevated Risk" if atr > 3 else "Moderate Risk" if atr > 1.5 else "Low Risk"
            })

        # Volume
        if obv_data.get("obv_trend"):
            # FIXED: More robust OBV interpretation logic
            price_trend_short = "up" if current_price > ma_data.get("MA_50", current_price) else "down"
            obv_trend = obv_data["obv_trend"]
            interpretation = "Not clear"
            if "trending" in obv_trend:
                if (price_trend_short == "up" and "↑" in obv_trend) or \
                   (price_trend_short == "down" and "↓" in obv_trend):
                    interpretation = "Volume confirms price trend"
                else:
                    interpretation = "Volume diverges from price trend"
            
            table_data.append({
                "category": "Volume",
                "metric": "OBV",
                "value": obv_data["obv_trend"],
                "interpretation": interpretation
            })
        return table_data

    # CHANGED: Added current_price to signature to check price vs MAs
    def _calculate_sentiment_score(self, current_price: float, technical_data: Dict) -> float:
        """Calculate overall sentiment score from technical indicators"""
        score = 0
        weights = 0
        rsi = technical_data.get("rsi")
        if rsi:
            if rsi < 30: score += 1.5 # Strong bullish
            elif rsi > 70: score -= 1.5 # Strong bearish
            elif rsi > 50: score += 0.5 # Mildly bullish
            elif rsi < 50: score -= 0.5 # Mildly bearish
            weights += 1.5

        macd_data = technical_data.get("macd", {})
        if macd_data.get("histogram"):
            score += 1 if macd_data["histogram"] > 0 else -1
            weights += 1

        ma_data = technical_data.get("moving_averages", {})
        if ma_data.get("MA_50") and ma_data.get("MA_200"):
            # Golden/Death cross is a strong, long-term signal
            score += 1.5 if ma_data["MA_50"] > ma_data["MA_200"] else -1.5
            weights += 1.5
        # Price vs short-term MA
        if ma_data.get("MA_50"):
            score += 1 if current_price > ma_data["MA_50"] else -1
            weights += 1

        stochastic = technical_data.get("stochastic", {})
        if stochastic.get("percent_k"):
            if stochastic["percent_k"] < 20: score += 1
            elif stochastic["percent_k"] > 80: score -= 1
            weights += 1
            
        obv_data = technical_data.get("obv", {})
        if obv_data.get("obv_trend"):
            if "↑" in obv_data["obv_trend"]: score += 1
            elif "↓" in obv_data["obv_trend"]: score -= 1
            weights += 1
            
        return score / weights if weights > 0 else 0

    def _get_sentiment_label(self, score: float) -> str:
        """Convert sentiment score to label"""
        if score >= 0.5: return "Strongly Bullish"
        if score > 0.2: return "Bullish"
        if score < -0.5: return "Strongly Bearish"
        if score < -0.2: return "Bearish"
        return "Neutral"

    def _generate_core_thesis(self, symbol: str, current_price: float, 
                              technical_data: Dict, sentiment: str) -> str:
        """Generate core thesis statement (fallback method)"""
        ma_data = technical_data.get("moving_averages", {})
        
        # FIXED: Use rupee symbol and correct logic
        if ma_data.get("MA_50") and current_price > ma_data.get("MA_50"):
            trend_signal = f"showing strength by trading above its 50-day MA (₹{ma_data['MA_50']:.2f})"
        elif ma_data.get("MA_50") and current_price < ma_data.get("MA_50"):
            trend_signal = f"facing headwinds below its 50-day MA (₹{ma_data['MA_50']:.2f})"
        else:
            trend_signal = "exhibiting mixed technical signals"
            
        if sentiment == "Bullish":
            direction = "suggesting potential for further upside."
        elif sentiment == "Bearish":
            direction = "indicating potential downside pressure."
        else:
            direction = "reflecting current market uncertainty."
        # FIXED: Removed dollar sign from symbol
        return f"{symbol} is currently {trend_signal}, {direction}"

    def _identify_bullish_signals(self, current_price: float, technical_data: Dict) -> list:
        """Identify bullish technical signals"""
        signals = []
        ma_data = technical_data.get("moving_averages", {})
        # FIXED: Use rupee symbol
        if ma_data.get("MA_50") and current_price > ma_data["MA_50"]:
            signals.append(f"Price is above the 50-day MA (₹{ma_data['MA_50']:.2f}), a positive short-term trend indicator.")
        if ma_data.get("MA_200") and current_price > ma_data["MA_200"]:
            signals.append(f"The stock is trading above its long-term 200-day MA (₹{ma_data['MA_200']:.2f}).")
        if rsi := technical_data.get("rsi"):
            if rsi < 30:
                signals.append(f"RSI at {rsi:.1f} is in oversold territory, suggesting a potential bounce.")
        if macd_data := technical_data.get("macd", {}):
            if macd_data.get("histogram", 0) > 0:
                signals.append("The MACD histogram is positive, indicating bullish momentum.")
        if obv_data := technical_data.get("obv", {}):
            if obv_data.get("obv_trend") == "↑ trending":
                signals.append("On-Balance Volume is trending upward, confirming price strength.")
        return signals if signals else ["No significant bullish signals identified."]

    def _identify_bearish_signals(self, current_price: float, technical_data: Dict) -> list:
        """Identify bearish technical signals"""
        signals = []
        ma_data = technical_data.get("moving_averages", {})
        # FIXED: Use rupee symbol
        if ma_data.get("MA_50") and current_price < ma_data["MA_50"]:
            signals.append(f"Price has fallen below the 50-day MA (₹{ma_data['MA_50']:.2f}), a bearish short-term signal.")
        if rsi := technical_data.get("rsi"):
            if rsi > 70:
                signals.append(f"RSI at {rsi:.1f} is overbought, suggesting the rally may be overextended.")
        if stochastic := technical_data.get("stochastic", {}):
            if stochastic.get("percent_k", 0) > 80:
                signals.append(f"Stochastic Oscillator at {stochastic['percent_k']:.1f} is in the overbought zone (>80).")
        if macd_data := technical_data.get("macd", {}):
            if macd_data.get("histogram", 0) < 0:
                signals.append("The MACD histogram is negative, indicating bearish momentum.")
        if obv_data := technical_data.get("obv", {}):
            if obv_data.get("obv_trend") == "↓ trending":
                signals.append("On-Balance Volume is trending downward, indicating distribution and weakness.")
        return signals if signals else ["No significant bearish signals identified."]

    def _interpret_rsi(self, rsi: float) -> str:
        """Interpret RSI value"""
        if rsi < 30:
            return "Oversold (Potentially Bullish)"
        elif rsi > 70:
            return "Overbought (Potentially Bearish)"
        elif rsi < 50:
            return "Below 50 (Bearish Momentum)"
        else:
            return "Above 50 (Bullish Momentum)"

    def _create_error_response(self, symbol: str, error_message: str) -> Dict[str, Any]:
        """Create error response when analysis fails"""
        return {
            "symbol": symbol,
            "error": True,
            "message": error_message,
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executive_summary": {
                "overall_sentiment": "Insufficient Data",
                "llm_generated_thesis": f"Unable to perform technical analysis for {symbol}: {error_message}",
                "key_levels": {
                    "support": None,
                    "resistance": None,
                    "confidence": "Low"
                }
            },
            "llm_generated_narrative_analysis": {
                "summary": "Insufficient data for analysis",
                "bullish_outlook": "Insufficient data for analysis",
                "bearish_outlook": "Insufficient data for analysis"
            },
            "data_table": []
        }