import zipfile
import pandas as pd
import os

# Currencies of interest
CURRENCY_NAMES = [
    'EURO FX', 'BRITISH POUND STERLING', 'JAPANESE YEN', 'SWISS FRANC',
    'CANADIAN DOLLAR', 'AUSTRALIAN DOLLAR', 'NEW ZEALAND DOLLAR'
]

def extract_txt_from_zip(zip_path, out_file="cot_latest.txt"):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for name in zip_ref.namelist():
            if name.endswith('.txt'):
                zip_ref.extract(name)
                os.rename(name, out_file)
                break

def parse_cot_txt(txt_path="cot_latest.txt"):
    df = pd.read_csv(txt_path, sep='\t', skiprows=1)
    df = df[df['Market_and_Exchange_Names'].isin(CURRENCY_NAMES)]
    cols = [
        "Report_Date_as_YYYY-MM-DD", "Market_and_Exchange_Names",
        "Noncommercial_Long_All", "Noncommercial_Short_All",
        "Commercial_Long_All", "Commercial_Short_All",
        "Open_Interest_All"
    ]
    df = df[cols]
    # Convert numbers
    df[[
        "Noncommercial_Long_All", "Noncommercial_Short_All", "Commercial_Long_All",
        "Commercial_Short_All", "Open_Interest_All"
    ]] = df[[
        "Noncommercial_Long_All", "Noncommercial_Short_All", "Commercial_Long_All",
        "Commercial_Short_All", "Open_Interest_All"
    ]].replace({',':''}, regex=True).astype(int)
    return df

if __name__ == "__main__":
    extract_txt_from_zip("cot_latest.zip")
    df = parse_cot_txt("cot_latest.txt")
    df.to_csv("cot_currencies.csv", index=False)
    print(df.tail())
