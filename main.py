import json
import os

import requests

from config import API_KEY, BASE_CURRENCY, DESTINATION_CURRENCY_SYMBOLS


def get_latest_rates(base: str = BASE_CURRENCY, destination_symbols: list = DESTINATION_CURRENCY_SYMBOLS):
    destination_symbols = ",".join(destination_symbols)
    url = f"https://api.apilayer.com/fixer/latest?symbols={destination_symbols}&base={base}"
    headers = {"apikey": API_KEY}

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.text)
    return None


def write_to_file(filename, content):
    os.makedirs("archive/", exist_ok=True)
    with open(f"archive/{filename}.json", "w") as f:
        f.write(json.dumps(content))


def create_filename(latest_rates_result):
    r = latest_rates_result
    filename = f"{r['base']}_{r['date']}_{r['timestamp']}"
    return filename


def main():
    result = get_latest_rates()
    filename = create_filename(result)
    content = result
    content.pop("success")
    write_to_file(filename=filename, content=content)


if __name__ == "__main__":
    main()
