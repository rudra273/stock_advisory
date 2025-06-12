import time
import functools
from typing import Callable, Any

def calculate_time(func: Callable) -> Callable:
    """
    Decorator that calculates and prints the execution time of a function.
    
    Args:
        func: The function to be decorated
        
    Returns:
        The wrapped function with timing functionality
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            
            print(f"Function '{func.__name__}' executed in {execution_time:.6f} seconds")
            return result
            
        except Exception as e:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            print(f"Function '{func.__name__}' failed after {execution_time:.6f} seconds")
            raise e
    
    return wrapper



from datetime import date
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

# from app.repositories.stock_metrics import get_all_metrics

from app.repositories.get_metrics import *
from app.repositories.calculated_metrics import *

# from app.repositories.stock_kpis import get_metrics_by_category

from app.repositories.optimized_stock_kpis import get_metrics_by_category

from app.db.config import SessionLocal  

# @calculate_time
def test_calculate_metrics():
    db = SessionLocal()
    try:
        symbol = "TCS.NS"
        period_date = date(2025, 3, 31)
        # result = get_all_direct_metrics(db, symbol)
        # result = calculate_all_metrics(db, symbol)
        result = get_metrics_by_category(db, symbol)
        # print(result)
        for i in result:
            print(i, result[i], end='\n\n')
    finally:
        db.close()


test_calculate_metrics()



# # Calculate ROE for specific date
# roe = calculate_roe(db, "AAPL", date(2024, 3, 31))

# # Calculate moving averages
# mas = calculate_moving_averages(db, "AAPL")  # Returns MA_50 and MA_200




