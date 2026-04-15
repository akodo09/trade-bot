# Prime Trade Terminal 

A production-quality Python CLI application for executing trades on the Binance Futures Testnet (USDT-M). This project focuses on clean architecture, excellent user experience, and robust logging.

## Features
- **Interactive CLI**: Powered by the `rich` library for a terminal workspace feel.
- **Robust Validation**: Ensures inputs (symbol, side, type, quantity, price) are validated before any API requests.
- **Dry-run Mode**: Ability to validate requests locally or simulate success without sending a live testnet order.
- **Resilience**: Features automatic retries for transient networking errors.
- **Structured Logging**: Clean log outputs saved asynchronously to `bot.log`.
- **Clean Architecture**: Strong SoC with isolated components acting independently (`engine`, `executor`, `validators`).

## Architecture Structure
- `engine.py`: Defines the lightweight `requests` HTTP wrapper for the Binance testnet and implements the HMAC signature protocol without dragging heavy SDKs along.
- `executor.py`: Composes the engine and dictates business logic (retries, logging hooks, and dry-run substitutions).
- `validators.py`: Isolated logic verifying the exact user inputs.
- `terminal.py`: The `rich`-based loop managing STDOUT/STDIN interactivity.
- `logger.py`: Global logging configuration.

## Setup
1. **Clone/Download** the repository.
2. **Install requirements**:
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure the Environment**:
   - Copy or rename `.env.example` to `.env`.
   - Populate `BINANCE_API_KEY` and `BINANCE_API_SECRET` with your API credentials from [Binance Futures Testnet](https://testnet.binancefuture.com).
   
## Running the Bot
Launch the trading terminal by executing:
```sh
python terminal.py
```

## Usage Example
1. Run `python terminal.py`
2. At the prompt `Enter Symbol (e.g., BTCUSDT)`: input **BTCUSDT**
3. At the prompt `Enter Side (BUY) / (SELL)`: input **BUY**
4. At the prompt `Enter Order Type (MARKET / LIMIT)`: input **LIMIT**
5. Enter Quantity (e.g., 0.05) and Price.
6. Choose whether to enable **Dry-Run Mode**.
7. Confirm the trade summary and review the formatted results panel.
