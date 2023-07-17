import typing
import abc
import dataclasses

"""
When I wrote this module I was experimenting with Google-style docstrings.
"""

@dataclasses.dataclass
class DBLoadResult:
    """
    Store the mechanism to get back cursor information on the number of rows inserted or
    encountered an error

    Attributes:
        number_of_rows_inserted: The number of rows inserted successfully in this transaction
        number_of_rows_updated: The number of rows updated successfully in this transaction
        number_of_error_rows: The number of rows that errored during the transaction.

    """

    number_of_rows_inserted: int = 0
    number_of_rows_updated: int = 0
    number_of_error_rows: int = 0


class AbstractDBConnector(abc.ABC):
    """
    Abstract database connector.

    For this exercise I'm going to implement both Postgres and BigQuery illustratively.

    Postgres will work easiest on my local, BigQuery will naturally scale better.
    """

    def __init__(self, **connect_kwargs: dict) -> None:
        """
        Establish a connection using the API for the database.
        Args:
            connect_kwargs: arguments used to init the DB API client
        """
        self.__dict__.update(connect_kwargs)

    @abc.abstractmethod
    def load_file_to_database(
        self, file_path: str, file_params: dict = None, **kwargs
    ) -> DBLoadResult:
        """
        For local testing, assume file paths in a local.
        If the file is in a cloud location, assume the file_path is a uri like ``s3::`` or ``gs::``

        Args:
            file_path: The file path or URI to a file.
            file_params: any parameters for reading the file.

        Returns:
            a :py:class:`db.connector.DBLoadResult` object with the number of rows inserted
            or errored
        """
        raise NotImplementedError


    @abc.abstractmethod
    def submit_sql(
        self, query: str, **kwargs
    ) -> typing.Union[typing.Generator[tuple, None, None], list]:
        """
        Issue SQL to the DB, retrieve a cursor of results or None if no results relevant given sql

        Args:
            query: an SQL query
            **kwargs: any execution-context

        """
        raise NotImplementedError
