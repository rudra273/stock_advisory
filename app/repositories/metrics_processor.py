# app/repositories/metrics_processor.py
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import date
import statistics

from app.repositories.helper import (
    get_current_price_by_symbol,
    get_stock_info_by_symbol,
    get_balance_sheets_by_symbol,
    get_income_statements_by_symbol,
    get_cash_flows_by_symbol,
    get_daily_prices_by_symbol,
    get_latest_financial_data,
    get_previous_period_data,
    safe_divide
)


class MetricsProcessor:
    """Centralized metrics processing with optimized data extraction and calculations"""
    
    def __init__(self, db: Session, symbol: str):
        self.db = db
        self.symbol = symbol.upper()
        self._cache = {}
    
    def _get_cached_data(self, data_type: str):
        """Cache database calls to avoid redundant queries"""
        if data_type not in self._cache:
            if data_type == 'current_price':
                self._cache[data_type] = get_current_price_by_symbol(self.db, self.symbol)
            elif data_type == 'stock_info':
                self._cache[data_type] = get_stock_info_by_symbol(self.db, self.symbol)
            elif data_type == 'balance_sheets':
                self._cache[data_type] = get_balance_sheets_by_symbol(self.db, self.symbol)
            elif data_type == 'income_statements':
                self._cache[data_type] = get_income_statements_by_symbol(self.db, self.symbol)
            elif data_type == 'cash_flows':
                self._cache[data_type] = get_cash_flows_by_symbol(self.db, self.symbol)
            elif data_type == 'daily_prices':
                self._cache[data_type] = get_daily_prices_by_symbol(self.db, self.symbol)
        return self._cache[data_type]
    
    def _safe_float(self, value) -> Optional[float]:
        """Safely convert to float"""
        return float(value) if value is not None else None
    
    def _safe_int(self, value) -> Optional[int]:
        """Safely convert to int"""
        return int(value) if value is not None else None
    
    def _safe_percentage(self, value) -> Optional[float]:
        """Safely convert to percentage"""
        return value * 100 if value is not None else None
    
    def get_current_price_metrics(self) -> Dict[str, Any]:
        """Get current price related metrics"""
        current_price = self._get_cached_data('current_price')
        
        if not current_price:
            return {
                "current_price": None,
                "previous_close": None,
                "change": None,
                "percent_change": None,
                "company_name": None
            }
        
        return {
            "current_price": current_price.currentPrice,
            "previous_close": current_price.previousClose,
            "change": current_price.Change,
            "percent_change": current_price.PercentChange,
            "company_name": current_price.companyName
        }
    
    def get_stock_info_metrics(self) -> Dict[str, Any]:
        """Get stock info metrics with optimized field extraction"""
        stock_info = self._get_cached_data('stock_info')
        
        if not stock_info:
            return self._get_empty_stock_info_dict()
        
        return {
            "short_name": stock_info.shortName,
            "currency": stock_info.currency,
            "sector": stock_info.sector,
            "industry": stock_info.industry,
            "previous_close": stock_info.previousClose,
            "regular_market_open": stock_info.regularMarketOpen,
            "day_low": stock_info.dayLow,
            "day_high": stock_info.dayHigh,
            "volume": self._safe_int(stock_info.volume),
            "trailing_eps": stock_info.trailingEps,
            "forward_eps": stock_info.forwardEps,
            "trailing_pe": stock_info.trailingPE,
            "forward_pe": stock_info.forwardPE,
            "dividend_rate": stock_info.dividendRate,
            "dividend_yield": self._safe_percentage(stock_info.dividendYield),
            "book_value": stock_info.bookValue,
            "price_to_book": stock_info.priceToBook,
            "price_to_sales": stock_info.priceToSalesTrailing12Months,
            "market_cap": self._safe_float(stock_info.marketCap),
            "enterprise_value": self._safe_float(stock_info.enterpriseValue),
            "beta": stock_info.beta,
            "trailing_peg_ratio": stock_info.trailingPegRatio,
            "return_on_equity": self._safe_percentage(stock_info.returnOnEquity),
            "return_on_assets": self._safe_percentage(stock_info.returnOnAssets),
            "profit_margins": self._safe_percentage(stock_info.profitMargins),
            "operating_margins": self._safe_percentage(stock_info.operatingMargins),
            "revenue_per_share": stock_info.revenuePerShare,
            "revenue_growth": self._safe_percentage(stock_info.revenueGrowth),
            "earnings_quarterly_growth": self._safe_percentage(stock_info.earningsQuarterlyGrowth),
            "total_debt": self._safe_float(stock_info.totalDebt),
            "total_cash": self._safe_float(stock_info.totalCash),
            "shares_outstanding": self._safe_float(stock_info.sharesOutstanding)
        }
    
    def get_balance_sheet_metrics(self, period_date: Optional[date] = None) -> Dict[str, Any]:
        """Get balance sheet metrics for specific or latest period"""
        balance_sheets = self._get_cached_data('balance_sheets')
        
        if not balance_sheets:
            return self._get_empty_balance_sheet_dict()
        
        balance_sheet = self._get_financial_statement(balance_sheets, period_date)
        
        if not balance_sheet:
            return self._get_empty_balance_sheet_dict()
        
        return {
            "date": balance_sheet.Date,
            "total_assets": self._safe_float(balance_sheet.total_assets),
            "total_debt": self._safe_float(balance_sheet.total_debt),
            "stockholders_equity": self._safe_float(balance_sheet.stockholders_equity),
            "cash_and_cash_equivalents": self._safe_float(balance_sheet.cash_and_cash_equivalents)
        }
    
    def get_income_statement_metrics(self, period_date: Optional[date] = None) -> Dict[str, Any]:
        """Get income statement metrics for specific or latest period"""
        income_statements = self._get_cached_data('income_statements')
        
        if not income_statements:
            return self._get_empty_income_statement_dict()
        
        income_stmt = self._get_financial_statement(income_statements, period_date)
        
        if not income_stmt:
            return self._get_empty_income_statement_dict()
        
        return {
            "date": income_stmt.Date,
            "total_revenue": self._safe_float(income_stmt.total_revenue),
            "gross_profit": self._safe_float(income_stmt.gross_profit),
            "operating_income": self._safe_float(income_stmt.operating_income),
            "net_income": self._safe_float(income_stmt.net_income),
            "basic_eps": income_stmt.basic_eps,
            "diluted_eps": income_stmt.diluted_eps
        }
    
    def get_cash_flow_metrics(self, period_date: Optional[date] = None) -> Dict[str, Any]:
        """Get cash flow metrics for specific or latest period"""
        cash_flows = self._get_cached_data('cash_flows')
        
        if not cash_flows:
            return self._get_empty_cash_flow_dict()
        
        cash_flow = self._get_financial_statement(cash_flows, period_date)
        
        if not cash_flow:
            return self._get_empty_cash_flow_dict()
        
        return {
            "date": cash_flow.Date,
            "operating_cash_flow": self._safe_float(cash_flow.operating_cash_flow),
            "capital_expenditure": self._safe_float(cash_flow.capital_expenditure),
            "free_cash_flow": self._safe_float(cash_flow.free_cash_flow),
            "cash_dividends_paid": self._safe_float(cash_flow.cash_dividends_paid)
        }
    
    def get_daily_prices_metrics(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get daily price metrics for technical analysis"""
        daily_prices = self._get_cached_data('daily_prices')
        
        if not daily_prices:
            return []
        
        sorted_prices = sorted(daily_prices, key=lambda x: x.Date, reverse=True)
        
        if limit:
            sorted_prices = sorted_prices[:limit]
        
        return [
            {
                "date": price.Date,
                "open": price.Open,
                "high": price.High,
                "low": price.Low,
                "close": price.Close,
                "volume": self._safe_int(price.Volume)
            }
            for price in sorted_prices
        ]
    
    def _get_financial_statement(self, statements: List, period_date: Optional[date]):
        """Generic method to get financial statement for specific or latest period"""
        if period_date:
            return next((stmt for stmt in statements if stmt.Date == period_date), None)
        return get_latest_financial_data(statements)
    
    def _get_empty_stock_info_dict(self) -> Dict[str, Any]:
        """Return empty stock info dictionary"""
        return {
            "short_name": None, "currency": None, "sector": None, "industry": None,
            "previous_close": None, "regular_market_open": None, "day_low": None,
            "day_high": None, "volume": None, "trailing_eps": None, "forward_eps": None,
            "trailing_pe": None, "forward_pe": None, "dividend_rate": None,
            "dividend_yield": None, "book_value": None, "price_to_book": None,
            "price_to_sales": None, "market_cap": None, "enterprise_value": None,
            "beta": None, "trailing_peg_ratio": None, "return_on_equity": None,
            "return_on_assets": None, "profit_margins": None, "operating_margins": None,
            "revenue_per_share": None, "revenue_growth": None, "earnings_quarterly_growth": None,
            "total_debt": None, "total_cash": None, "shares_outstanding": None
        }
    
    def _get_empty_balance_sheet_dict(self) -> Dict[str, Any]:
        """Return empty balance sheet dictionary"""
        return {
            "date": None, "total_assets": None, "total_debt": None,
            "stockholders_equity": None, "cash_and_cash_equivalents": None
        }
    
    def _get_empty_income_statement_dict(self) -> Dict[str, Any]:
        """Return empty income statement dictionary"""
        return {
            "date": None, "total_revenue": None, "gross_profit": None,
            "operating_income": None, "net_income": None, "basic_eps": None,
            "diluted_eps": None
        }
    
    def _get_empty_cash_flow_dict(self) -> Dict[str, Any]:
        """Return empty cash flow dictionary"""
        return {
            "date": None, "operating_cash_flow": None, "capital_expenditure": None,
            "free_cash_flow": None, "cash_dividends_paid": None
        }


class CalculatedMetrics:
    """Handles all calculated financial ratios and technical indicators"""
    
    def __init__(self, metrics_processor: MetricsProcessor):
        self.processor = metrics_processor
    
    def calculate_debt_to_equity_ratio(self, period_date: Optional[date] = None) -> Optional[float]:
        """Calculate Debt-to-Equity ratio"""
        balance_sheet = self.processor.get_balance_sheet_metrics(period_date)
        total_debt = balance_sheet.get("total_debt")
        stockholders_equity = balance_sheet.get("stockholders_equity")
        return safe_divide(total_debt, stockholders_equity)
    
    def calculate_earnings_yield(self) -> Optional[float]:
        """Calculate earnings yield (inverse of P/E ratio)"""
        stock_info = self.processor.get_stock_info_metrics()
        pe_ratio = stock_info.get("trailing_pe")
        if pe_ratio and pe_ratio > 0:
            return (1 / pe_ratio) * 100
        return None
    
    def calculate_payout_ratio(self, period_date: Optional[date] = None) -> Optional[float]:
        """Calculate dividend payout ratio"""
        cash_flow = self.processor.get_cash_flow_metrics(period_date)
        income_statement = self.processor.get_income_statement_metrics(period_date)
        
        dividends_paid = cash_flow.get("cash_dividends_paid")
        net_income = income_statement.get("net_income")
        
        if not dividends_paid or not net_income:
            return None
        
        dividends_paid = abs(dividends_paid)
        payout_ratio = safe_divide(dividends_paid, net_income)
        return payout_ratio * 100 if payout_ratio is not None else None
    
    def calculate_debt_ratio(self, period_date: Optional[date] = None) -> Optional[float]:
        """Calculate debt ratio"""
        balance_sheet = self.processor.get_balance_sheet_metrics(period_date)
        total_debt = balance_sheet.get("total_debt")
        total_assets = balance_sheet.get("total_assets")
        return safe_divide(total_debt, total_assets)
    
    def calculate_gross_margin(self, period_date: Optional[date] = None) -> Optional[float]:
        """Calculate gross profit margin"""
        income_statement = self.processor.get_income_statement_metrics(period_date)
        gross_profit = income_statement.get("gross_profit")
        total_revenue = income_statement.get("total_revenue")
        
        if not gross_profit or not total_revenue:
            return None
        
        margin = safe_divide(gross_profit, total_revenue)
        return margin * 100 if margin is not None else None
    
    def calculate_asset_turnover(self, current_date: Optional[date] = None) -> Optional[float]:
        """Calculate asset turnover ratio"""
        balance_sheets = self.processor._get_cached_data('balance_sheets')
        income_statements = self.processor._get_cached_data('income_statements')
        
        if not income_statements or not balance_sheets or len(balance_sheets) < 2:
            return None
        
        if current_date:
            income_stmt = next((stmt for stmt in income_statements if stmt.Date == current_date), None)
            current_bs = next((bs for bs in balance_sheets if bs.Date == current_date), None)
            previous_bs = get_previous_period_data(balance_sheets, current_date)
        else:
            income_stmt = get_latest_financial_data(income_statements)
            sorted_bs = sorted(balance_sheets, key=lambda x: x.Date, reverse=True)
            current_bs = sorted_bs[0]
            previous_bs = sorted_bs[1] if len(sorted_bs) > 1 else None
        
        if not income_stmt or not current_bs or not previous_bs:
            return None
        
        if not income_stmt.total_revenue or not current_bs.total_assets or not previous_bs.total_assets:
            return None
        
        avg_assets = (float(current_bs.total_assets) + float(previous_bs.total_assets)) / 2
        return safe_divide(income_stmt.total_revenue, avg_assets)
    
    def calculate_equity_multiplier(self, current_date: Optional[date] = None) -> Optional[float]:
        """Calculate equity multiplier"""
        balance_sheets = self.processor._get_cached_data('balance_sheets')
        
        if not balance_sheets or len(balance_sheets) < 2:
            return None
        
        if current_date:
            current_bs = next((bs for bs in balance_sheets if bs.Date == current_date), None)
            previous_bs = get_previous_period_data(balance_sheets, current_date)
        else:
            sorted_bs = sorted(balance_sheets, key=lambda x: x.Date, reverse=True)
            current_bs = sorted_bs[0]
            previous_bs = sorted_bs[1] if len(sorted_bs) > 1 else None
        
        if not current_bs or not previous_bs:
            return None
        
        if not current_bs.total_assets or not previous_bs.total_assets or not current_bs.stockholders_equity or not previous_bs.stockholders_equity:
            return None
        
        avg_assets = (float(current_bs.total_assets) + float(previous_bs.total_assets)) / 2
        avg_equity = (float(current_bs.stockholders_equity) + float(previous_bs.stockholders_equity)) / 2
        
        return safe_divide(avg_assets, avg_equity)
    
    def calculate_volatility(self, days: int = 252) -> Optional[float]:
        """Calculate historical price volatility"""
        daily_prices = self.processor._get_cached_data('daily_prices')
        
        if not daily_prices or len(daily_prices) < 2:
            return None
        
        sorted_prices = sorted(daily_prices, key=lambda x: x.Date, reverse=True)
        if len(sorted_prices) > days:
            sorted_prices = sorted_prices[:days]
        
        sorted_prices.reverse()
        
        returns = []
        for i in range(1, len(sorted_prices)):
            if sorted_prices[i-1].Close and sorted_prices[i].Close:
                daily_return = (sorted_prices[i].Close - sorted_prices[i-1].Close) / sorted_prices[i-1].Close
                returns.append(daily_return)
        
        if len(returns) < 2:
            return None
        
        volatility = statistics.stdev(returns)
        annualized_volatility = volatility * (252 ** 0.5)
        return annualized_volatility * 100
    
    def calculate_moving_averages(self, periods: List[int] = [50, 200]) -> Dict[str, Optional[float]]:
        """Calculate moving averages for specified periods"""
        daily_prices = self.processor._get_cached_data('daily_prices')
        
        if not daily_prices:
            return {f"MA_{period}": None for period in periods}
        
        sorted_prices = sorted(daily_prices, key=lambda x: x.Date, reverse=True)
        
        result = {}
        for period in periods:
            if len(sorted_prices) >= period:
                recent_prices = sorted_prices[:period]
                valid_prices = [price.Close for price in recent_prices if price.Close is not None]
                
                if len(valid_prices) == period:
                    ma = sum(valid_prices) / len(valid_prices)
                    result[f"MA_{period}"] = ma
                else:
                    result[f"MA_{period}"] = None
            else:
                result[f"MA_{period}"] = None
        
        return result
    
    def calculate_rsi(self, periods: int = 14) -> Optional[float]:
        """Calculate Relative Strength Index (RSI)"""
        daily_prices = self.processor._get_cached_data('daily_prices')
        
        if not daily_prices or len(daily_prices) < periods + 1:
            return None
        
        sorted_prices = sorted(daily_prices, key=lambda x: x.Date, reverse=True)[:periods + 1]
        sorted_prices.reverse()
        
        gains = []
        losses = []
        
        for i in range(1, len(sorted_prices)):
            if sorted_prices[i-1].Close and sorted_prices[i].Close:
                change = sorted_prices[i].Close - sorted_prices[i-1].Close
                if change > 0:
                    gains.append(change)
                    losses.append(0)
                else:
                    gains.append(0)
                    losses.append(abs(change))
        
        if len(gains) < periods:
            return None
        
        avg_gain = sum(gains[-periods:]) / periods
        avg_loss = sum(losses[-periods:]) / periods
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def get_all_ratios(self, period_date: Optional[date] = None) -> Dict[str, Any]:
        """Calculate all financial ratios"""
        return {
            "debt_to_equity": self.calculate_debt_to_equity_ratio(period_date),
            "earnings_yield": self.calculate_earnings_yield(),
            "payout_ratio": self.calculate_payout_ratio(period_date),
            "debt_ratio": self.calculate_debt_ratio(period_date),
            "gross_margin": self.calculate_gross_margin(period_date),
            "asset_turnover": self.calculate_asset_turnover(period_date),
            "equity_multiplier": self.calculate_equity_multiplier(period_date)
        }
    
    def get_all_technical_indicators(self) -> Dict[str, Any]:
        """Calculate all technical analysis indicators"""
        return {
            "volatility": self.calculate_volatility(),
            "moving_averages": self.calculate_moving_averages(),
            "rsi": self.calculate_rsi()
        }
    
    # Add these methods to your CalculatedMetrics class in metrics_processor.py

    def calculate_macd(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Dict[str, Optional[float]]:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        daily_prices = self.processor._get_cached_data('daily_prices')
        
        if not daily_prices or len(daily_prices) < slow_period:
            return {"macd": None, "signal": None, "histogram": None, "crossover_date": None}
        
        sorted_prices = sorted(daily_prices, key=lambda x: x.Date, reverse=True)
        
        # Get closing prices
        closes = [price.Close for price in sorted_prices if price.Close is not None]
        
        if len(closes) < slow_period:
            return {"macd": None, "signal": None, "histogram": None, "crossover_date": None}
        
        # Calculate EMAs
        def calculate_ema(prices, period):
            multiplier = 2 / (period + 1)
            ema = [prices[0]]  # Start with first price
            
            for i in range(1, len(prices)):
                ema_value = (prices[i] * multiplier) + (ema[-1] * (1 - multiplier))
                ema.append(ema_value)
            
            return ema
        
        # Reverse for chronological order
        closes.reverse()
        
        if len(closes) >= slow_period:
            fast_ema = calculate_ema(closes, fast_period)
            slow_ema = calculate_ema(closes, slow_period)
            
            # Calculate MACD line
            macd_line = []
            for i in range(len(fast_ema)):
                if i < slow_period - 1:
                    macd_line.append(0)
                else:
                    macd_line.append(fast_ema[i] - slow_ema[i])
            
            # Calculate Signal line (EMA of MACD)
            macd_values = [x for x in macd_line if x != 0]
            if len(macd_values) >= signal_period:
                signal_line = calculate_ema(macd_values, signal_period)
                
                # Calculate histogram
                current_macd = macd_line[-1]
                current_signal = signal_line[-1]
                histogram = current_macd - current_signal
                
                # Check for recent crossover (last 5 days)
                crossover_date = None
                if len(signal_line) >= 2:
                    prev_histogram = macd_line[-2] - signal_line[-2] if len(signal_line) > 1 else 0
                    if (prev_histogram <= 0 and histogram > 0) or (prev_histogram >= 0 and histogram < 0):
                        crossover_date = sorted_prices[-1].Date
                
                return {
                    "macd": current_macd,
                    "signal": current_signal,
                    "histogram": histogram,
                    "crossover_date": crossover_date
                }
        
        return {"macd": None, "signal": None, "histogram": None, "crossover_date": None}

    def calculate_stochastic_oscillator(self, k_period: int = 14, d_period: int = 3) -> Dict[str, Optional[float]]:
        """Calculate Stochastic Oscillator (%K and %D)"""
        daily_prices = self.processor._get_cached_data('daily_prices')
        
        if not daily_prices or len(daily_prices) < k_period:
            return {"percent_k": None, "percent_d": None}
        
        sorted_prices = sorted(daily_prices, key=lambda x: x.Date, reverse=True)[:k_period + d_period]
        
        # Calculate %K
        recent_prices = sorted_prices[:k_period]
        
        current_close = recent_prices[0].Close
        if current_close is None:
            return {"percent_k": None, "percent_d": None}
        
        # Find highest high and lowest low in the period
        highest_high = max([p.High for p in recent_prices if p.High is not None])
        lowest_low = min([p.Low for p in recent_prices if p.Low is not None])
        
        if highest_high == lowest_low:
            percent_k = 50  # Avoid division by zero
        else:
            percent_k = ((current_close - lowest_low) / (highest_high - lowest_low)) * 100
        
        # Calculate %D (moving average of %K)
        # For simplicity, we'll calculate %D as a 3-period average of %K values
        k_values = []
        for i in range(min(d_period, len(sorted_prices) - k_period + 1)):
            subset = sorted_prices[i:i + k_period]
            close = subset[0].Close
            if close is not None:
                high = max([p.High for p in subset if p.High is not None])
                low = min([p.Low for p in subset if p.Low is not None])
                if high != low:
                    k_val = ((close - low) / (high - low)) * 100
                    k_values.append(k_val)
        
        percent_d = sum(k_values) / len(k_values) if k_values else None
        
        return {
            "percent_k": percent_k,
            "percent_d": percent_d
        }

    def calculate_atr(self, period: int = 14) -> Optional[float]:
        """Calculate Average True Range (ATR) for volatility measurement"""
        daily_prices = self.processor._get_cached_data('daily_prices')
        
        if not daily_prices or len(daily_prices) < period + 1:
            return None
        
        sorted_prices = sorted(daily_prices, key=lambda x: x.Date, reverse=True)[:period + 1]
        sorted_prices.reverse()  # Chronological order
        
        true_ranges = []
        
        for i in range(1, len(sorted_prices)):
            current = sorted_prices[i]
            previous = sorted_prices[i-1]
            
            if all([current.High, current.Low, previous.Close]):
                tr1 = current.High - current.Low
                tr2 = abs(current.High - previous.Close)
                tr3 = abs(current.Low - previous.Close)
                
                true_range = max(tr1, tr2, tr3)
                true_ranges.append(true_range)
        
        if len(true_ranges) >= period:
            atr = sum(true_ranges[-period:]) / period
            # Return as percentage of current price
            current_price = sorted_prices[-1].Close
            if current_price:
                return (atr / current_price) * 100
        
        return None

    def calculate_obv(self) -> Dict[str, Any]:
        """Calculate On-Balance Volume (OBV) and its trend"""
        daily_prices = self.processor._get_cached_data('daily_prices')
        
        if not daily_prices or len(daily_prices) < 2:
            return {"obv": None, "obv_trend": None}
        
        sorted_prices = sorted(daily_prices, key=lambda x: x.Date, reverse=True)
        sorted_prices.reverse()  # Chronological order
        
        obv = 0
        obv_values = [0]
        
        for i in range(1, len(sorted_prices)):
            current = sorted_prices[i]
            previous = sorted_prices[i-1]
            
            if current.Close and previous.Close and current.Volume:
                if current.Close > previous.Close:
                    obv += current.Volume
                elif current.Close < previous.Close:
                    obv -= current.Volume
                # If close == previous close, OBV stays the same
                
                obv_values.append(obv)
        
        # Determine trend (last 10 periods)
        trend_period = min(10, len(obv_values))
        if trend_period >= 2:
            recent_obv = obv_values[-trend_period:]
            if len(recent_obv) >= 2:
                trend_slope = (recent_obv[-1] - recent_obv[0]) / (len(recent_obv) - 1)
                if trend_slope > 0:
                    obv_trend = "↑ trending"
                elif trend_slope < 0:
                    obv_trend = "↓ trending"
                else:
                    obv_trend = "→ sideways"
            else:
                obv_trend = "insufficient data"
        else:
            obv_trend = "insufficient data"
        
        return {
            "obv": obv,
            "obv_trend": obv_trend
        }

    def identify_support_resistance_levels(self) -> Dict[str, Any]:
        """Identify key support and resistance levels"""
        daily_prices = self.processor._get_cached_data('daily_prices')
        
        if not daily_prices or len(daily_prices) < 20:
            return {"support": None, "resistance": None, "confidence": "Low"}
        
        # Get last 60 days of data for better level identification
        sorted_prices = sorted(daily_prices, key=lambda x: x.Date, reverse=True)[:60]
        
        current_price = sorted_prices[0].Close
        if not current_price:
            return {"support": None, "resistance": None, "confidence": "Low"}
        
        # Find significant highs and lows
        highs = []
        lows = []
        
        for i, price in enumerate(sorted_prices):
            if price.High and price.Low:
                # Look for local maxima and minima
                if i > 2 and i < len(sorted_prices) - 2:
                    # Check if it's a local high
                    if (price.High > sorted_prices[i-1].High and 
                        price.High > sorted_prices[i-2].High and
                        price.High > sorted_prices[i+1].High and 
                        price.High > sorted_prices[i+2].High):
                        highs.append(price.High)
                    
                    # Check if it's a local low
                    if (price.Low < sorted_prices[i-1].Low and 
                        price.Low < sorted_prices[i-2].Low and
                        price.Low < sorted_prices[i+1].Low and 
                        price.Low < sorted_prices[i+2].Low):
                        lows.append(price.Low)
        
        # Find resistance (closest significant high above current price)
        resistance_levels = [h for h in highs if h > current_price]
        resistance = min(resistance_levels) if resistance_levels else None
        
        # Find support (closest significant low below current price)
        support_levels = [l for l in lows if l < current_price]
        support = max(support_levels) if support_levels else None
        
        # Determine confidence based on how many times levels were tested
        confidence = "Moderate"
        if len(highs) >= 3 and len(lows) >= 3:
            confidence = "High"
        elif len(highs) < 2 or len(lows) < 2:
            confidence = "Low"
        
        return {
            "support": support,
            "resistance": resistance,
            "confidence": confidence
        }

    def get_comprehensive_technical_analysis(self) -> Dict[str, Any]:
        """Get all technical analysis indicators in one call"""
        return {
            "moving_averages": self.calculate_moving_averages([50, 200]),
            "rsi": self.calculate_rsi(),
            "macd": self.calculate_macd(),
            "stochastic": self.calculate_stochastic_oscillator(),
            "atr": self.calculate_atr(),
            "obv": self.calculate_obv(),
            "volatility": self.calculate_volatility(),
            "support_resistance": self.identify_support_resistance_levels()
        }