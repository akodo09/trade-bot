import time
import hmac
import hashlib
from urllib.parse import urlencode
import requests
from typing import Dict, Any

from logger import get_logger

class BinanceEngine:
    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.logger = get_logger("BinanceEngine")

    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def _prepare_headers(self) -> Dict[str, str]:
        return {
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = 0.0, test: bool = False) -> Dict[str, Any]:
        endpoint = "/fapi/v1/order/test" if test else "/fapi/v1/order"
        url = f"{self.BASE_URL}{endpoint}"

        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": str(quantity),
            "timestamp": int(time.time() * 1000)
        }

        if order_type.upper() == "LIMIT":
            params["price"] = str(price)
            params["timeInForce"] = "GTC"

        query_string = urlencode(params)
        signature = self._generate_signature(query_string)
        payload = f"{query_string}&signature={signature}"

        self.logger.info(f"Sending request to {endpoint} with payload: {params}")

        response = requests.post(
            url,
            headers=self._prepare_headers(),
            data=payload
        )

        response.raise_for_status()
        return response.json()
