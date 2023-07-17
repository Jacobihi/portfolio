import os
import csv
import requests

from bs4 import BeautifulSoup, element

DEFAULT_DIRECTORY = os.path.join('/Users', os.environ["USER"], 'Downloads')

TABLE = 'table'
HEADER_TAG = 'th'
TABLE_ROW_TAG = 'tr'
CELL_DATA_TAG = 'td'
TITLE = 'title'
DELIMITER = ','


def write_webpage_tables_to_csv(
    url: str = None, file_path: str = None, destination_directory: str = DEFAULT_DIRECTORY
):
    """
    Given a URL or a file_path with HTML, write in the directory (defaults to downloads for Mac users)
    by parsing each table on the page into csv.

    Usage:

    .. code-block:: shell

       cli utilities write_webpage_tables_to_csv \\
       --url "https://en.wikipedia.org/wiki/Slowly_changing_dimension"

    Results in 21 csv files in Downloads folder; one file per table in the doc.

    """
    if not os.path.exists(destination_directory):
        print(f"{destination_directory} doesn't exist, aborting mission")
        return None
    if url:
        response = requests.get(url)
        html_doc = response.text
    elif file_path and file_path.endswith('.html'):
        with open(file_path, 'r') as x:
            html_doc = x.read()
    else:
        raise FileNotFoundError("No url or HTML file_path specified, aborting mission")

    soup = BeautifulSoup(html_doc, 'html.parser')
    tables = soup.find_all(TABLE)
    table_files = []
    for table_index, table in enumerate(tables):
        table_csv_file = _print_table_to_csv(
            table=table, n=table_index, directory=destination_directory
        )
        table_files.append(table_csv_file)
        print(table_csv_file)
    return table_files


def _print_table_to_csv(
    table: element.Tag, n: int = 0, title: str = None, directory: str = None, file_path: str = None
):
    """Given a 'table' element, check for header, render row data, call it a day"""
    headers = table.find_all(HEADER_TAG)
    if headers:
        headers = [h.text for h in headers]
    rows = table.find_all(TABLE_ROW_TAG)[1:] if headers else table.find_all(TABLE_ROW_TAG)
    title = title or table.attrs.get(TITLE, f"table_{n}")
    file_path = file_path or os.path.join(directory, f"{title}.csv")
    with open(file_path, 'w') as csv_object:
        writer = csv.writer(
            csv_object,
            dialect='excel',
            delimiter=DELIMITER,
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        if headers:
            writer.writerow(headers)
        for row in rows:
            row_data = row.find_all(CELL_DATA_TAG)
            writer.writerow([cell.text.strip() for cell in row_data])
    return file_path
