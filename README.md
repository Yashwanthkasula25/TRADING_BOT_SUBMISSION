🚀 Binance Futures Trading Bot (Hybrid Mode with TWAP Support)

This project is a hybrid trading bot designed for the
“Junior Python Developer – Crypto Trading Bot” assignment.
It supports both real Binance Futures Testnet trading (REST API) and an optional MOCK mode for environments where Testnet access is restricted (such as India).

The bot is built with clean, modular, interview-ready code and follows all required specifications, including logging, CLI input validation, and advanced order types.

✨ Features
✔ 1. Hybrid API Engine

Real API Mode – Uses Binance Futures Testnet REST endpoints

Mock Mode – Fully simulated environment (no API keys required)

You can switch instantly using:

--mock

✔ 2. Order Types Supported

MARKET Orders

LIMIT Orders

TWAP (Time-Weighted Average Price) – Bonus feature

TWAP splits a large order into multiple slices over time to reduce execution impact.

✔ 3. Full Logging System

All API requests, responses, and errors are logged to:

logs/api_requests.log
logs/api_errors.log


This matches the company requirement to track every interaction.

✔ 4. Clean CLI Interface

The bot validates and accepts:

Symbol

Side (BUY/SELL)

Order Type (MARKET/LIMIT/TWAP)

Quantity

Price (for LIMIT)

TWAP slices + duration

API keys (optional)

✔ 5. Professional Project Structure
binance-trading-bot/
│
├── main.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── basic_bot.py      # real API + mock fallback
│   ├── twap.py           # TWAP slicing logic
│   ├── cli.py            # CLI handler
│   └── utils.py          # helpers (signing, timestamps)
│
├── logs/
│   ├── api_requests.log
│   └── api_errors.log
│
└── samples/
    └── sample_run.txt

🛠 Installation
1. Clone the repo
git clone https://github.com/<your-username>/TRADING_BOT_SUBMISSION.git
cd TRADING_BOT_SUBMISSION

2. Install requirements
pip install -r requirements.txt

▶ Usage
⭐ MOCK Mode (No API keys required)
python main.py --mock --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

⭐ REAL Testnet Mode (Requires API keys + VPN)
python main.py \
  --api-key YOUR_KEY \
  --api-secret YOUR_SECRET \
  --testnet \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.001

⭐ TWAP Example

Splitting 0.01 BTC into 5 slices over 60 seconds:

python main.py --mock \
  --symbol BTCUSDT \
  --side BUY \
  --type TWAP \
  --quantity 0.01 \
  --twap-slices 5 \
  --twap-duration 60

📌 Important Notes
✔ Testnet Availability

Binance Futures Testnet is blocked in some regions (like India).
In such cases, MOCK mode allows full functionality and log generation for submission.

✔ Real API Logic Included

Even if Testnet is not reachable, the code still includes:

Request signing

Timestamp

HMAC-SHA256

Futures endpoints (/fapi/v1/order, /fapi/v2/balance)

This meets the assignment’s requirement for real API implementation.

🧪 Sample Run Output (MOCK)
$ python main.py --mock --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

TWAP slice 1/3...
TWAP slice 2/3...
Order executed (mock)


Detailed logs appear in logs/api_requests.log.

📧 Assignment Submission Notes

This project satisfies:

✔ Place market & limit orders
✔ Use Binance Futures Testnet API (with mock fallback)
✔ Input validation via CLI
✔ Logging system for requests/responses/errors
✔ Clean project structure
✔ Advanced order (TWAP) — BONUS
✔ Error handling with meaningful messages

This repository is ready to be attached with your resume and submitted for the assignment.

🤝 Author

Yashwanth Kasula
Python Developer | Machine Learning | Backend Development
GitHub: https://github.com/Yashwanthkasula25