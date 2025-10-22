import sys
import update_portfolio
import generate_summary

def run_production_pipeline():
    """
    Runs the full production data pipeline:
    1. Updates portfolio (ETL)
    2. Generates summary report
    """
    print("Starting Pokémon Pipeline!", file = sys.stderr)
    print("Running update_portfolio.main() ", file = sys.stderr)
    update_portfolio.main()
    print("Running generate_summary.main() ", file = sys.stderr)
    generate_summary.main()

if __name__ == "__main__":
    run_production_pipeline()