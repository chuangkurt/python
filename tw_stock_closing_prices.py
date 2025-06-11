import csv
import requests
from datetime import datetime
from typing import List, Tuple


def fetch_closing_prices(date: str) -> List[Tuple[str, str, float]]:
    """Fetch closing prices for all TWSE stocks on a given date.

    Parameters
    ----------
    date : str
        Date in YYYYMMDD format, e.g. '20240102'.

    Returns
    -------
    List[Tuple[str, str, float]]
        A list of (stock_id, stock_name, closing_price).
    """
    url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL"
    params = {
        "response": "json",
        "date": date,
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    fields = data.get("fields", [])
    if not fields:
        raise ValueError("Fields not found in response")
    closing_idx = fields.index("收盤價")

    result = []
    for row in data.get("data", []):
        stock_id = row[0].strip()
        stock_name = row[1].strip()
        closing_price = float(row[closing_idx].replace(",", ""))
        result.append((stock_id, stock_name, closing_price))
    return result


def save_to_csv(rows: List[Tuple[str, str, float]], file_path: str) -> None:
    """Save the rows to a CSV file."""
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Stock ID", "Name", "Close"])
        writer.writerows(rows)


def main():
    date = datetime.now().strftime("%Y%m%d")
    rows = fetch_closing_prices(date)
    save_to_csv(rows, f"twse_closing_prices_{date}.csv")


if __name__ == "__main__":
    main()
