# Binance Futures Trading Bot — Hybrid (Real API + MOCK) with TWAP

This project implements a hybrid trading bot: it includes full Binance Futures Testnet REST API logic with a MOCK fallback. It supports MARKET and LIMIT orders, BUY/SELL sides, request/response logging, and an optional TWAP order type (bonus).

## Structure
```
binance-trading-bot/
├─ README.md
├─ requirements.txt
├─ main.py
├─ src/
│  ├─ basic_bot.py
│  ├─ twap.py
│  ├─ cli.py
│  └─ utils.py
├─ logs/
│  ├─ api_requests.log
│  └─ api_errors.log
└─ samples/
   └─ sample_run.txt
```
## How to run
- Install: `pip install -r requirements.txt`
- Mock mode (no API keys required):
```
python main.py --mock --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```
- Real mode (needs Binance Futures Testnet keys):
```
python main.py --api-key KEY --api-secret SECRET --testnet --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```
- TWAP example (mock):
```
python main.py --mock --symbol BTCUSDT --side BUY --type TWAP --quantity 0.01 --twap-slices 5 --twap-duration 60
```
## Notes
- If you are geographically blocked from testnet (e.g., India), use `--mock` or run behind a VPN and create a testnet account at https://testnet.binancefuture.com
- The project logs requests/responses to `logs/api_requests.log` and errors to `logs/api_errors.log`.
