import requests

COT_URL = "https://www.cftc.gov/files/dea/history/fut_fin_txt_2024.zip"

def fetch_cot_report(out_file="cot_latest.zip"):
    response = requests.get(COT_URL)
    if response.status_code == 200:
        with open(out_file, "wb") as f:
            f.write(response.content)
        print("Downloaded latest COT data.")
    else:
        raise Exception(f"Failed to download. Status {response.status_code}")

if __name__ == "__main__":
    fetch_cot_report()
