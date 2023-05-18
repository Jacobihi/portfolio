import os
from pyspark.sql import SparkSession


def lambda_handler(event, context):
    """
    The spark.config items are from https://plainenglish.io/blog/spark-on-aws-lambda-c65877c0ac96
    """
    print(context)
    file_path = event.get("file_path")
    s3_path = event.get("s3_path")

    file_kwargs = event.get("file_kwargs") or {}
    spark = SparkSession.builder.appName("spark-on-lambda-demo")

    if s3_path and not file_path:
        (
            spark.config("spark.hadoop.fs.s3a.access.key", os.environ['AWS_ACCESS_KEY_ID'])
            .config("spark.hadoop.fs.s3a.secret.key", os.environ['AWS_SECRET_ACCESS_KEY'])
            .config("spark.hadoop.fs.s3a.session.token", os.environ['AWS_SESSION_TOKEN'])
        )
    spark = spark.getOrCreate()
    q = spark.read.csv(file_path, **file_kwargs)
    spark.stop()
    return {'statusCode': 200, 'body': q.columns}

