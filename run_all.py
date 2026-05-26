import fetch_cot_data
import parse_cot_data
import cot_analysis


def main():
    print("Fetching latest COT report...")
    fetch_cot_data.fetch_cot_report()

    print("Unzipping and parsing COT data...")
    parse_cot_data.extract_txt_from_zip("cot_latest.zip")
    df = parse_cot_data.parse_cot_txt("cot_latest.txt")
    df.to_csv("cot_currencies.csv", index=False)

    print("Analyzing COT data and generating advanced institutional signals...")
    adv_signals = cot_analysis.advanced_signals(df)
    adv_signals.to_csv("advanced_signals.csv", index=False)
    print("Advanced signals saved in advanced_signals.csv\n")
    print(adv_signals)

if __name__ == "__main__":
    main()
