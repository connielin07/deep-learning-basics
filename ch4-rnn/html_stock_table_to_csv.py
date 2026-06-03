from __future__ import annotations

import argparse
import csv
import re
from html.parser import HTMLParser
from pathlib import Path


COLUMNS = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
SPLIT_DATE = "Aug 25, 2022"


class TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: list[list[str]] = []
        self._current_row: list[str] | None = None
        self._current_cell: list[str] | None = None
        self._in_cell = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tr":
            self._current_row = []
        elif tag in {"td", "th"} and self._current_row is not None:
            self._current_cell = []
            self._in_cell = True

    def handle_data(self, data: str) -> None:
        if self._in_cell and self._current_cell is not None:
            self._current_cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self._current_row is not None and self._current_cell is not None:
            text = re.sub(r"\s+", " ", "".join(self._current_cell)).strip()
            self._current_row.append(text)
            self._current_cell = None
            self._in_cell = False
        elif tag == "tr" and self._current_row is not None:
            if self._current_row:
                self.rows.append(self._current_row)
            self._current_row = None


def parse_stock_rows(html_path: Path) -> list[list[str]]:
    html = html_path.read_text(encoding="utf-8")
    parser = TableParser()
    parser.feed(html)

    split_present = "3:1" in html and "Stock Splits" in html and SPLIT_DATE in html
    stock_rows: list[list[str]] = []

    for row in parser.rows:
        if len(row) != len(COLUMNS):
            continue
        if row[0] == "Date":
            continue
        if split_present and row[0] == SPLIT_DATE:
            continue

        volume = row[6].replace(",", "")
        if not volume.isdigit():
            continue

        stock_rows.append([*row[:6], int(volume)])

    return stock_rows


def convert_file(html_path: Path) -> Path:
    csv_path = html_path.with_suffix(".csv")
    rows = parse_stock_rows(html_path)

    with csv_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(COLUMNS)
        writer.writerows(rows)

    return csv_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Yahoo Finance stock-price HTML tables to CSV.")
    parser.add_argument("html_files", nargs="+", type=Path)
    args = parser.parse_args()

    for html_file in args.html_files:
        csv_path = convert_file(html_file)
        print(f"{html_file} -> {csv_path}")


if __name__ == "__main__":
    main()
