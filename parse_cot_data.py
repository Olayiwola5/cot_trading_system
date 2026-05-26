import zipfile
import csv
import os

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

def parse_cot_txt(txt_path="cot_latest.txt", out_csv="cot_currencies.csv"):
    rows = []
    with open(txt_path, newline='', encoding="utf-8") as infile:
        reader = csv.DictReader(infile, delimiter='\t')
        for row in reader:
            if row["Market_and_Exchange_Names"] in CURRENCY_NAMES:
                # Convert numeric fields
                for f in ["Noncommercial_Long_All", "Noncommercial_Short_All", "Commercial_Long_All", "Commercial_Short_All", "Open_Interest_All"]:
                    t = row[f].replace(',', '')
                    row[f] = int(t) if t != '' else 0
                rows.append(row)
    # Write to CSV
    if out_csv:
        with open(out_csv, "w", newline='', encoding="utf-8") as out:
            writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    return rows

if __name__ == "__main__":
    extract_txt_from_zip("cot_latest.zip")
    parse_cot_txt("cot_latest.txt", "cot_currencies.csv")
    print("Parsed and saved filtered COT data.")
