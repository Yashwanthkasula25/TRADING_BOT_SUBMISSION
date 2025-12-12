import argparse, logging, os
from .basic_bot import BasicBot
from .twap import run_twap

logger = logging.getLogger('basicbot')
logger.setLevel(logging.INFO)
if not logger.handlers:
    import sys, logging as _logging
    h = _logging.StreamHandler(sys.stdout)
    h.setLevel(_logging.INFO)
    logger.addHandler(h)

def parse_args():
    p = argparse.ArgumentParser(description='Hybrid Binance Futures Trading Bot (Testnet)')
    p.add_argument('--api-key', help='API Key (optional, for real testnet)')
    p.add_argument('--api-secret', help='API Secret (optional)')
    p.add_argument('--testnet', action='store_true', help='Use testnet base URL (default True if not provided)')
    p.add_argument('--mock', action='store_true', help='Force mock mode (no network)')
    p.add_argument('--base-url', help='Override base URL')
    p.add_argument('--symbol', required=True, help='Symbol e.g. BTCUSDT')
    p.add_argument('--side', required=True, choices=['BUY','SELL','buy','sell'], help='BUY or SELL')
    p.add_argument('--type', required=True, choices=['MARKET','LIMIT','TWAP','market','limit','twap'], help='Order type')
    p.add_argument('--quantity', type=float, required=True, help='Quantity (base units)')
    p.add_argument('--price', type=float, help='Price for LIMIT slices')
    p.add_argument('--time-in-force', default='GTC', choices=['GTC','IOC','FOK'], help='TIF for LIMIT')
    p.add_argument('--twap-slices', type=int, default=5, help='TWAP slices')
    p.add_argument('--twap-duration', type=int, default=60, help='TWAP total duration seconds')
    return p.parse_args()

def run_cli():
    args = parse_args()
    api_key = args.api_key
    api_secret = args.api_secret
    mock = args.mock or (not api_key or not api_secret)
    bot = BasicBot(api_key=api_key, api_secret=api_secret, testnet=args.testnet, base_url=args.base_url, mock=mock)
    symbol = args.symbol.upper()
    side = args.side.upper()
    ord_type = args.type.upper()
    qty = args.quantity
    price = args.price
    tif = args.time_in_force
    try:
        logger.info('Checking server time...')
        st = bot.get_server_time()
        logger.info('Server time: %s', st)
    except Exception as e:
        logger.exception('Time check failed: %s', e)
    if ord_type == 'MARKET':
        res = bot.place_order(symbol=symbol, side=side, ord_type='MARKET', quantity=qty)
        print(res)
    elif ord_type == 'LIMIT':
        if price is None:
            raise SystemExit('LIMIT orders require --price')
        res = bot.place_order(symbol=symbol, side=side, ord_type='LIMIT', quantity=qty, price=price, time_in_force=tif)
        print(res)
    elif ord_type == 'TWAP':
        res_list = run_twap(bot=bot, symbol=symbol, side=side, quantity=qty, slices=args.twap_slices, duration=args.twap_duration, ord_type='MARKET', price=price)
        for r in res_list:
            print(r)
    else:
        raise SystemExit('Unsupported order type')
