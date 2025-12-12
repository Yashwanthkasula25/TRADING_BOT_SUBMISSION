import requests, logging, time, json
from typing import Optional, Dict, Any, Tuple
from urllib.parse import urlencode
from .utils import sign, now_ms

logger = logging.getLogger('basicbot')
logger.setLevel(logging.INFO)

class MockBinanceClient:
    order_id = 10000
    def futures_change_leverage(self, symbol, leverage):
        logger.info(f"[MOCK] Leverage set -> {symbol} @ {leverage}x")
        return {"symbol": symbol, "leverage": leverage, "status": "SUCCESS"}
    def futures_create_order(self, symbol, side, type, quantity, **kwargs):
        MockBinanceClient.order_id += 1
        order = {"symbol": symbol, "side": side, "type": type, "origQty": quantity, "price": kwargs.get('price','MARKET'), "status": "FILLED", "orderId": MockBinanceClient.order_id, "clientOrderId": f"mock-{MockBinanceClient.order_id}"}
        logger.info(f"[MOCK] Order placed -> {order}")
        return order

class BasicBot:
    def __init__(self, api_key: Optional[str]=None, api_secret: Optional[str]=None, testnet: bool=True, base_url: Optional[str]=None, mock: bool=False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.mock = mock or (api_key is None or api_secret is None)
        self.testnet = testnet
        self.base_url = base_url or ("https://testnet.binancefuture.com" if testnet else "https://fapi.binance.com")
        headers = {"X-MBX-APIKEY": api_key} if api_key else {}
        self.headers = headers
        if self.mock:
            self.client = MockBinanceClient()
            logger.info("Initialized BasicBot in MOCK mode")
        else:
            self.session = requests.Session()
            self.session.headers.update(self.headers)
            logger.info(f"Initialized BasicBot (testnet={self.testnet}) base_url={self.base_url}")
    def _log(self, method: str, path: str, params: dict, resp: Optional[requests.Response]):
        try:
            logger.info(f"REQUEST -> {method} {path} | params={params}")
            if resp is not None:
                logger.info(f"RESPONSE <- status={resp.status_code} body={resp.text}")
        except Exception as e:
            logger.exception("Logging error: %s", e)
    def _signed_request(self, method: str, path: str, params: dict) -> Tuple[Optional[Dict[str,Any]], Optional[requests.Response]]:
        if self.mock:
            logger.info("Mock signed request: skipping network call")
            return {"mock": True}, None
        try:
            params = params.copy()
            params['timestamp'] = now_ms()
            query_string = urlencode(params, doseq=True)
            signature = sign(self.api_secret, query_string)
            query_string = query_string + "&signature=" + signature
            url = self.base_url + path + "?" + query_string
            if method.upper() == 'GET':
                resp = self.session.get(url, timeout=20)
            elif method.upper() == 'POST':
                resp = self.session.post(url, timeout=20)
            elif method.upper() == 'DELETE':
                resp = self.session.delete(url, timeout=20)
            else:
                raise ValueError('Unsupported method')
            self._log(method, path, params, resp)
            try:
                return resp.json(), resp
            except Exception:
                return {"raw": resp.text}, resp
        except requests.RequestException as e:
            logger.exception('Network error: %s', e)
            return None, None
    def ping(self):
        if self.mock:
            return {}
        data, _ = self._signed_request('GET', '/fapi/v1/ping', {})
        return data
    def get_server_time(self):
        if self.mock:
            return {"serverTime": now_ms()}
        data, _ = self._signed_request('GET', '/fapi/v1/time', {})
        return data
    def place_order(self, symbol: str, side: str, ord_type: str, quantity: float, price: Optional[float]=None, time_in_force: str='GTC', reduce_only: bool=False, close_position: bool=False) -> Dict[str,Any]:
        symbol = symbol.upper()
        side = side.upper()
        ord_type = ord_type.upper()
        if ord_type not in ('MARKET','LIMIT'):
            raise ValueError('ord_type must be MARKET or LIMIT')
        params = {"symbol": symbol, "side": side, "type": ord_type, "quantity": float(quantity), "recvWindow": 5000}
        if ord_type == 'LIMIT':
            if price is None:
                raise ValueError('price required for LIMIT')
            params['price'] = float(price)
            params['timeInForce'] = time_in_force
        if self.mock:
            return self.client.futures_create_order(symbol=symbol, side=side, type=ord_type, quantity=quantity, price=(price if price else 'MARKET'))
        data, resp = self._signed_request('POST', '/fapi/v1/order', params)
        if resp is not None and not resp.ok:
            logger.error('API error: %s', data)
        return data if data is not None else {"error": "no_response"}
    def set_leverage(self, symbol: str, leverage: int):
        if self.mock:
            return self.client.futures_change_leverage(symbol, leverage)
        params = {"symbol": symbol.upper(), "leverage": int(leverage)}
        data, resp = self._signed_request('POST', '/fapi/v1/leverage', params)
        return data
    def place_twap(self, symbol: str, side: str, total_quantity: float, slices: int, duration_seconds: int, ord_type_for_slice: str='MARKET', price: Optional[float]=None, time_in_force: str='GTC'):
        if slices <= 0:
            raise ValueError('slices must be >=1')
        slice_qty = float(total_quantity) / slices
        wait = float(duration_seconds) / max(1, (slices - 1)) if slices > 1 else 0
        results = []
        for i in range(slices):
            logger.info(f"TWAP slice {i+1}/{slices}: qty={slice_qty}")
            try:
                res = self.place_order(symbol=symbol, side=side, ord_type=ord_type_for_slice, quantity=round(slice_qty,8), price=price, time_in_force=time_in_force)
                results.append(res)
            except Exception as e:
                logger.exception('TWAP slice error: %s', e)
                results.append({"error": str(e)})
            if i != slices-1:
                time.sleep(wait)
        return results
    def get_account_balance(self):
        if self.mock:
            return [{"asset":"USDT","balance":10000}]
        data, resp = self._signed_request('GET', '/fapi/v2/balance', {})
        return data
