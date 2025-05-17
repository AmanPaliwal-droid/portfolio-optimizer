# Portfolio Optimizer (0/1 Knapsack)

## Project Overview
This project implements a portfolio optimizer using dynamic programming (0/1 knapsack) to select assets maximizing expected return under capital and risk constraints. It reads market data from CSV files, applies optimization, and visualizes the efficient frontier (risk vs return).

## Features
- Reads asset data from CSV (Ticker, Expected Return, Risk Score, Price).
- Uses dynamic programming for 0/1 knapsack optimization by capital.
- Applies a risk filter to meet risk tolerance constraints.
- Sweeps risk tolerance levels to plot an efficient frontier.
- Command-line interface with arguments for capital, risk tolerance, input CSV, and plotting.
- Unit tests verifying optimization logic.
- Generates a scatter plot of risk vs expected return saved as `frontier.png`.

## Usage
Run the optimizer from command line:

```bash
python optimizer.py --capital 75000 --risk 35 --csv assets.csv --plot
