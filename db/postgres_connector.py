import csv
import os
import typing

import sqlalchemy
from sqlalchemy.exc import ResourceClosedError

from cli.logger import get_logger
from db.abstract_connector import AbstractDBConnector, DBLoadResult

logger = get_logger('postgres_logger')


LOCAL_CONN_STRING = 'LOCAL_CONN_STRING'
SCHEMA_KEY = 'schema'
TABLE_KEY = 'table'


class PostgresConnector(AbstractDBConnector):
    """
    Use sqlalchemy's psycopg2 driver for Postgres.
    Psycopg2 has the advantage of copy_expert, which is a super fast way to load and pull data.
    """

    def __init__(self, **connect_kwargs: dict):
        """
        Create a client to run Postgres queries with.

        For my purposes, I'll be using the password in ~/.pgpass.

        I have my local DB connections in an environment variable LOCAL_CONN_STRING

        Args:
            dbname

        """
        logger.info("creating postgres connector")

        self.conn_string = connect_kwargs.pop("conn_string", None) or os.environ.get(
            LOCAL_CONN_STRING
        )
        if not self.conn_string:
            raise ValueError("You need a connection string for Postgres connector")
        super().__init__(**connect_kwargs)

    def load_file_to_database(
        self, file_path: str, file_params: dict = None, **kwargs
    ) -> DBLoadResult:
        """
        Use copy expert method to load the file to the table for staging queries.

        Usage:

        .. code-block:: python

           connector = PostgresConnector()
           connector.load_file_to_database(file_path='path/to/file.csv', schema='schema', table='table')

        Args
            file_path:
            file_params (dict, optional):
            schema (str): the schema to load into
            table (str): the table to load into
            dsn or conn_string: a psycopg2 connstring, formatted differently from Sql Alchemy

        Returns

        """
        engine = sqlalchemy.create_engine(self.conn_string)
        table = kwargs.get(TABLE_KEY)
        schema = kwargs.get(SCHEMA_KEY)
        logger.info(f"Loading from {file_path} into {schema}.{table}")
        delimiter = kwargs.get('delimiter', ',')
        header = get_header_from_csv(file_path=file_path, delimiter=delimiter)
        quote_headers = [f'"{h}"' for h in header]
        header_string = f"({', '.join(quote_headers)})"
        # TODO: Add remainder of the copy options.
        sql = (
            f'COPY {schema}.{table} {header_string} FROM stdin '
            f'WITH CSV HEADER DELIMITER AS \'{delimiter}\''
        )

        connection = engine.raw_connection()
        cursor = connection.cursor()
        with open(file_path, 'r') as f:
            cursor.copy_expert(sql=sql, file=f)
            number_of_rows_affected = cursor.rowcount
        connection.close()
        result = DBLoadResult(number_of_rows_inserted=number_of_rows_affected)
        logger.info(f"{number_of_rows_affected} rows affected")
        return result

    def submit_sql(
        self, query: str, **kwargs
    ) -> typing.Union[typing.Generator[tuple, None, None], list]:
        """
        This currently just returns all results at once, but could be optimized
        for pagination

        Args:
            query: an SQL query
            dml (Optional, bool): Defaulst to False, if True commit the transaction
            **kwargs: any execution-context

        """
        mode = kwargs.get('mode', 'yield')
        query = sqlalchemy.text(query)
        engine = sqlalchemy.create_engine(self.conn_string, future=True)
        with engine.connect() as connection:
            results = connection.execute(query)
            connection.commit()
            try:
                if mode != 'yield':
                    results = [tuple(results.keys())] + [r for r in results]
                logger.info(f"{results.rowcount}")

                if mode == 'yield':
                    yield tuple(results.keys())
                    for row in results:
                        yield row
            except ResourceClosedError:
                logger.info("No rows returned, cursor closed")
                yield ()
            finally:
                engine.dispose()
                if mode != 'yield':
                    return results


def get_header_from_csv(file_path: str, delimiter: str = ',') -> list:
    """
    Return the headers from a CSV as a list.

    Helpful for running copy commands when you need to know the list of columns to load correctly.

    Args:
        file_path: the file path to a csv.
        delimiter: the files delimiter, defaults to ','

    Returns:

    """
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, dialect='excel', delimiter=delimiter)
        header = next(reader)
    return header
