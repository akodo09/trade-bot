import time
from typing import Dict, Any, Tuple
from requests.exceptions import RequestException

from engine import BinanceEngine
from logger import get_logger

class OrderExecutor:
    def __init__(self, engine: BinanceEngine):
        self.engine = engine
        self.logger = get_logger("OrderExecutor")
        self.max_retries = 2

    def execute(self, symbol: str, side: str, order_type: str, quantity: float, price: float, dry_run: bool) -> Tuple[bool, Dict[str, Any], str]:
        retries = 0
        while retries <= self.max_retries:
            try:
                self.logger.info(f"Attempt {retries + 1} to place order. Dry-run: {dry_run}")
                
                response = self.engine.place_order(
                    symbol=symbol,
                    side=side,
                    order_type=order_type,
                    quantity=quantity,
                    price=price,
                    test=dry_run
                )
                
                if dry_run:
                    response = {"orderId": "DRY-RUN-SIMULATED", "status": "TEST_SUCCESS"}
                    
                self.logger.info(f"Order executed successfully: {response}")
                return True, response, "Success"
                
            except RequestException as e:
                self.logger.error(f"Network or API error: {e}")
                err_msg = str(e)
                if hasattr(e, "response") and e.response is not None:
                    try:
                        err_msg = e.response.json().get("msg", err_msg)
                        self.logger.error(f"API Error Message: {err_msg}")
                    except ValueError:
                        pass
                
                retries += 1
                if retries <= self.max_retries:
                    self.logger.info("Retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    self.logger.error("Max retries reached. Failing.")
                    return False, {}, err_msg
            except Exception as e:
                self.logger.exception(f"Unexpected error: {e}")
                return False, {}, str(e)
        
        return False, {}, "Unknown error"
