import os
from db.postgres_connector import PostgresConnector


def load_a_file_to_postgres(file_path: str, tables: list, schema: str, conn_string: str = None,
                            delimiter: str = ','):
    """Wrapper of the postgres connector's load method.
    This seemed like the fastest way to prove a database task using my command line utility.
    """
    conn_string = conn_string or os.environ.get('LOCAL_CONN_STRING')
    connector = PostgresConnector(conn_string=conn_string)
    for table in tables:
        connector.load_file_to_database(file_path=file_path, schema=schema, table=table, delimiter=delimiter)
