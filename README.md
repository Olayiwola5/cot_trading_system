# COT Institutional Trading System

This project automatically fetches CFTC Commitments of Traders (COT) data for Forex currency pairs, applies institutional-grade analytics, and generates actionable trade signals.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the complete workflow:
   ```bash
   python run_all.py
   ```

- Output: `signals.csv` and `advanced_signals.csv` – trade directions for major FX pairs.

## Files
- `fetch_cot_data.py`: Downloads & saves the latest COT report.
- `parse_cot_data.py`: Parses COT data and focuses on major currency pairs.
- `cot_analysis.py`: Computes net positions, COT index, and generates signals with advanced institutional logic.
- `run_all.py`: Orchestrates the workflow end-to-end.
- `requirements.txt`: All dependencies.
