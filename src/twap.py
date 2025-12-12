from typing import List, Dict, Any
from .basic_bot import BasicBot

def run_twap(bot: BasicBot, symbol: str, side: str, quantity: float, slices: int, duration: int, ord_type: str='MARKET', price: float=None):
    return bot.place_twap(symbol=symbol, side=side, total_quantity=quantity, slices=slices, duration_seconds=duration, ord_type_for_slice=ord_type, price=price)
