import typing

from google.cloud import bigquery
import pandas as pd
import pandas_gbq

PROJECT_ID = 'project_id'
TABLE_ID = 'table_id'
WRITE_DISPOSITION = 'write_disposition'
WRITE_TRUNCATE = 'WRITE_TRUNCATE'
WRITE_APPEND = 'WRITE_APPEND'
WRITE_EMPTY = 'WRITE_EMPTY'


class BigQueryConnector:
    """
    Create a simple connector object to help me internalize the behavior of GCP relative
    to other DB connections I've used from sqlalchemy.

    BigQuery is columnar and therefore behaves differently from an optimization standpoint than
    RDBMS. It is more akin to Redshift.

    BigQuery has native support for Geometry datatype for geospatial visualizations.

    I can connect locally to the BigQuery client using the GOOGLE_APPLICATION_CREDENTIALS
    environment variable.

    In production, would use `ADC <https://cloud.google.com/docs/authentication/provide
    -credentials-adc>`_

    I have done some basic connecting and querying to gain familiarity.

    I plan to prove a few examples over time using this as a replaceable storage engine.

    This is why it is framed with some abstract connection methods so I can ultimately
    have a runner call some ETL irrespective of the data engine.
    """

    def __init__(self, **connect_kwargs: dict):
        """
        Create a client to run BigQuery queries with.

        Args:
            project_id: the project_id of the project your instance lives in.

        """
        self.project_id = connect_kwargs.pop(PROJECT_ID, None)
        if not self.project_id:
            raise ValueError("You must enter a project ID to use DB Connector methods for BigQuery")

        self.client = bigquery.Client()

    def load_file_to_database(
        self, file_path: str, file_params: dict = None, **kwargs
    ):
        """
        A common ETL task is to receive some file from somewhere and load it into the DB.
        This is just a simplified method for that.

        References:
            * Batch load from local: https://cloud.google.com/bigquery/docs/batch-loading-data
            #loading_data_from_local_files
            * See also https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud
            .bigquery.job.LoadJobConfig
            * in the future, this could be more flexible with https://cloud.google.com/bigquery/docs/reference/standard-sql/other-statements#load_data_statement
        or https://cloud.google.com/bigquery/docs/cloud-storage-transfer

        This is currently only implemented as a proof-of-concept.

        Args:
            file_path: file path to load from
            file_params: any parameters for reading the file.
            table_id: your_project_id.your_dataset.your_table_name
            write_disposition: one of WRITE_TRUNCATE, WRITE_APPEND, WRITE_EMPTY; defaults to
                               WRITE_APPEND

        """
        table_id = kwargs.get(TABLE_ID)
        write_disposition = kwargs.get(WRITE_DISPOSITION, WRITE_APPEND)

        if not table_id:
            raise ValueError(
                f"You must submit a table Id of the form 'your_project_id.your_dataset.your_table_name'"
            )
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            write_disposition=write_disposition,
        )

        with open(file_path, "rb") as source_file:
            job = self.client.load_table_from_file(source_file, table_id, job_config=job_config)

        job.result()
        table = self.client.get_table(table_id)

    def load_cursor_results_to_dataframe(self, query: str) -> pd.DataFrame:
        """
        Was experimenting with pandas_gbq given pandas ubiquity.

        Args:
            query: GoogleSQL query to execute against a BigQuery instance

        Returns:
            a pandas DataFrame loading the big query results.
        """
        return pandas_gbq.read_gbq(query, project_id=self.project_id)

    def load_dataframe_to_db(
        self, data_frame: pd.DataFrame, table: str, **kwargs
    ) :
        """
        use the pandas-gbq to_bq

        Args:
            data_frame: a data frame from any system
            table: the table name to load to (project_id.dataset.table_id)
            **kwargs: other args of pandas_gbq .to_gbq

        Returns:
            the result if possible (hard to get in BQ at moment)
        """
        pandas_gbq.to_gbq(dataframe=data_frame, destination_table=table, **kwargs)

    def submit_sql(self, query: str, **kwargs) -> typing.Generator:
        """
        Yield all the rows from a query result.

        Args:
            query: an SQL query
            **kwargs: any execution-context

        """
        query_job = self.client.query(query, **kwargs)
        results = query_job.result()

        for row in results:
            yield row
