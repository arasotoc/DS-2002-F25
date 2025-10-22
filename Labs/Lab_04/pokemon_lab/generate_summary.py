import pandas as pd
import os
import sys

def generate_summary(portfolio_file):
    """
    Reads the portfolio CSV and prints total value + most valuable card.
    """
    if not os.path.exists(portfolio_file):
        print(f"Error: File '{portfolio_file}' not found.", file = sys.stderr)
        sys.exit(1)

    df = pd.read_csv(portfolio_file)

    if df.empty:
        print("The portfolio file is empty.")
        return
    
    total_value = df["card_market_value"].sum()
    most_valuable = df.loc[df["card_market_value"].idxmax()]

    print("\n===== Pokémon Portfolio Summary =====")
    print(f"Total Portfolio Value: ${total_value:,.2f}")
    print("------------------------------------")
    print(f"Most Valuable Card: {most_valuable['card_name']}")
    print(f"Card ID: {most_valuable['card_id']}")
    print(f"Market Value: ${most_valuable['card_market_value']:,.2f}")
    print("====================================\n")

def main():
    generate_summary("card_portfolio.csv")

def test():
    generate_summary("test_card_portfolio.csv")

if __name__ == "__main__":
    print("Running Summary Script Test Mode...", file = sys.stderr)
    test()