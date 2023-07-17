"""
This is a random collection of utilities that I have found useful in the past.
"""
import os
import csv


def turn_csv_into_markdown_table(file_path: str, output_file: str = None):
    """
    Produce a markdown table from a CSV file.

    Emulate functionality like from https://www.tablesgenerator.com/markdown_tables
    Follow the standard as defined https://www.markdownguide.org/extended-syntax/

    Assumes you have a csv generated from excel so it encodes to utf-8-sig and also strips the
    column names in the header.

    .. warning::

       Text in your CSV cannot contain the `|` pipe character or newlines.

    Usage (mac example):

    .. code-block:: shell

       file_path='/path/to/table_name.csv'
       output_file="/path/to/table_name.md"
       cli utilities  turn_csv_into_markdown_table \\
            --file_path "${file_path}" \\
            --output_file "${output_file}" \\
            > /dev/stderr | pbcopy

    The above is a Mac-based example in which you print the markdown to console, write to file,
    and copy to clipboard.

    :param file_path: the CSV file path in question, by default we assume it's named the table
    :param output_file: if you want to write the table to file you can do so

    """

    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f, dialect='excel')
        columns = [x.strip() for x in next(reader)]
        rows = [row for row in reader]
    column_length_map = []
    header = '| '
    separator_line = '\n| '
    for index, header_name in enumerate(columns):
        width = max([max([len(row[index]) for row in rows]), len(header_name), 3])
        column_length_map.append(width)
        header_name_length = len(header_name)
        gap = width - header_name_length
        header = f'{header}{header_name}{" " * gap} | '
        separator_line = f"{separator_line}{'-' * width} | "
    markdown_text = f"{header}{separator_line}"
    for row in rows:
        row_text = '\n| '
        for index, cell in enumerate(row):
            width = column_length_map[index]
            cell_length = len(cell)
            gap = width - cell_length
            row_text = f"{row_text}{cell}{' ' * gap} | "
        markdown_text += row_text

    print(markdown_text)
    if output_file:
        with open(output_file, 'w') as f:
            f.write(markdown_text)
    return markdown_text


def turn_csv_into_select_from_values_statement(
    file_path: str, table_name: str = None, output_file: str = None, mode: str = 'SELECT'
):
    """
    Lightweight utility to read a CSV and turn it into either  a SELECT FROM VALUES statement OR
    to go whole-hog with ``mode`` == ``INSERT`` and write a full-on INSERT INTO statement

    Assumes you have a csv generated from excel so it encodes to utf-8-sig and also strips the
    column names in the header.

    This is very helpful when you want to mockup data in Excel or Sheets and then run it in an
    arbitrary SQL console.

    .. note:: Note about Datatypes

       This utility forces everything as a string literal value, so you'll have to modify the
       select statement to format any thing with different types or nulls or whatever

    Usage:

    .. code-block:: shell

       file_path='/path/to/table_name.csv'
       output_file="/path/to/table_name.sql"
       cli utillities  turn_csv_into_select_from_values_statement \\
            --file_path "${file_path}" \\
            --mode insert \\
            --output_file "${output_file}" \\
            > /dev/stderr | pbcopy

    The above is a Mac-based example in which you print the sql to console, write to file, and copy
    to clipboard.

    It would turn a csv like the following:

    .. csv-table:: table_name.csv
       :header: "id", "name", "status"
       :widths: 5, 10, 10

       1, "John", "active"
       2, "Jane", "inactive"
       3, "Jill", "active"

    Into a SQL statement like the following:

    .. code-block:: sql

         INSERT INTO table_name (id, name, status)
         SELECT column1 AS id, column2 AS name, column3 AS status
         FROM (VALUES
            ('1', 'John', 'active'),
            ('2', 'Jane', 'inactive'),
            ('3', 'Jill', 'active')
            ) AS raw_values

    :param file_path: the CSV file path in question, by default we assume it's named the table
    :param table_name: if different from your CSV file, the explicit table name to insert into
    :param output_file: if you want to write this SELECT statement to file, the output file
           path
    :param mode: Defaults to ``SELECT`` as in just select from values, but could be ``INSERT`` to
                 wrap the whole thing in INSERT INTO TABLE (columns) SELECT columns FROM values

    """
    table_name = table_name or os.path.basename(file_path).replace(".csv", "")
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f, dialect='excel')
        columns = [x.strip() for x in next(reader)]
        my_sql_statement = ''
        if mode.upper() == 'INSERT':
            my_sql_statement = f'INSERT INTO {table_name} ({", ".join(columns)})' + "\n"
        select_elements = ', '.join(
            [f"column{n+1} AS {column}" for n, column in enumerate(columns)]
        )
        my_sql_statement = f"{my_sql_statement}SELECT {select_elements} FROM (VALUES\n"
        row_joiner = '\n, '
        processed_rows = [
            '({list_of_cols})'.format(
                list_of_cols=', '.join(
                    ["'{target}'".format(target=cell.replace("'", "\\'")) for cell in row]
                )
            )
            for row in reader
        ]

        my_sql_statement = f"{my_sql_statement}{row_joiner.join(processed_rows)}"
    my_sql_statement = f"{my_sql_statement}\n) AS raw_values"
    print(my_sql_statement)
    if output_file:
        with open(output_file, 'w') as f:
            f.write(my_sql_statement)
    return my_sql_statement
