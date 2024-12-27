# Arbitrage Betting Project

## Table of Contents

- [Motivation](#motivation)
- [Project Structure](#project-structure)
- [How to Run the Project](#how-to-run-the-project)
- [Dependencies](#dependencies)
- [Arbitrage Mathematics](#arbitrage-mathematics)
- [Arbitrage Profit Margin](#arbitrage-profit-margin)
- [Betting Unit Calculation](#betting-unit-calculation)
- [Note](#note)

## Motivation

The **Arbitrage Betting** project is a Python tool designed to identify arbitrage opportunities in sports betting. Arbitrage allows for a guaranteed profit by placing bets on all possible outcomes of a sporting event, exploiting differences in odds between various bookmakers.

## Project Structure

- `fetch_data.py`: Retrieves sports data and odds via an API.
- `find_arbitrage.py`: Contains the logic to identify arbitrage opportunities based on the retrieved odds.
- `main.py`: The main entry point to run the program.
- `sports_mapping.py`: Maps sport keys to their full names and descriptions.
- `config.py`: Contains the API key configuration.

## How to Run the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/Keracles/arbitrage-betting.git
   cd arbitrage-betting
   ```

2. Install the dependencies:

   ```bash
   pip install requests
   ```

3. Configure your API key:

   - Generate your own API key from [The Odds API](https://the-odds-api.com/).
   - Open `config.py` and add your API key:

     ```python
     API_KEY = "your_api_key_here"
     ```

4. Run the main script:

   ```bash
   python main.py
   ```

## Dependencies

- Python 3.x
- `requests` library: Install it by running `pip install requests`

## Arbitrage Mathematics

To determine if an arbitrage opportunity exists, we use the following formula:

$$
\text{Arbitrage Profit Margin} = \left( \frac{1}{\text{Best Home Odds}} + \frac{1}{\text{Best Away Odds}} \right)
$$

If the sum of the inverses of the best odds for each outcome (home and away) is less than 1, an arbitrage opportunity exists. The smaller the sum, the higher the potential profit.

**Example:**

If we have:

- Best Home Odds = 2.00
- Best Away Odds = 2.50

The arbitrage profit margin would be:

$$
\text{Arbitrage Profit Margin} = \left( \frac{1}{2.00} + \frac{1}{2.50} \right) = 0.9
$$

Since 0.9 < 1, this is an arbitrage opportunity.

## Arbitrage Profit Margin

The arbitrage profit margin indicates the guaranteed return on investment. A margin less than 1 indicates a profitable arbitrage opportunity. The exact profit can be calculated as follows:

$$
\text{Profit} = \left( \frac{1}{\text{Arbitrage Profit Margin}} - 1 \right) \times 100\%
$$

For the example above:

$$
\text{Profit} = \left( \frac{1}{0.9} - 1 \right) \times 100\% = 11.11\%
$$

This means you can expect a return of 11.11% on your total bet amount.

## Betting Unit Calculation

Suppose you want to bet a total of 1 unit. You need to determine how to allocate this unit between the home and away bets to guarantee a profit.

If we have:

- Best Home Odds = 2.00
- Best Away Odds = 2.50

1. Calculate the raw units to bet based on the odds:

   - Raw units on Home Team = 1 / 2.00 = 0.5
   - Raw units on Away Team = 1 / 2.50 = 0.4

2. The sum of the raw units is: 0.5 + 0.4 = 0.9

3. To ensure you bet the total unit, adjust proportionally:

   - Adjusted units on Home Team = 0.5 / 0.9 ≈ 0.556
   - Adjusted units on Away Team = 0.4 / 0.9 ≈ 0.444

This means you should bet approximately 0.556 units on the home team and 0.444 units on the away team for a profit of 0.11 units per unit bet.

## Note

- This project currently supports only H2H (moneyline) markets. 
