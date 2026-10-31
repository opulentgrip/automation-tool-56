# automation-tool-56

A high-performance Python framework designed to automate liquidity provision and order execution across decentralized exchanges. It leverages asynchronous execution to minimize latency and maximize capital efficiency in volatile market conditions.

## Features

*   **Multi-DEX Support:** Native integration for Uniswap V3 and PancakeSwap, with support for custom contract interactions via Web3.py.
*   **Asynchronous Engine:** Utilizes `asyncio` for non-blocking websocket streaming of real-time price feeds and order book updates.
*   **Risk Management Suite:** Configurable trailing stop-loss, take-profit triggers, and gas-fee optimization thresholds.
*   **State Persistence:** Integrated SQLite logging to track historical trade performance and slippage metrics for strategy backtesting.

## Installation

Ensure you have Python 3.10+ installed. Clone the repository and install the dependencies:

```bash
git clone https://github.com/Developer/automation-tool-56.git
cd automation-tool-56
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Basic Usage

Configure your environment variables in `.env` before initiating the bot. Run the execution engine using the following command:

```bash
# Set your private key and RPC endpoint in .env first
python main.py --strategy scalper --pair ETH-USDT --leverage 2
```

To run the backtesting module on local data logs:

```bash
python backtester.py --file logs/trade_history.db --format json
```

## License

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.