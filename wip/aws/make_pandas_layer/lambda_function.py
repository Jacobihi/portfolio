import pandas as pd
import boto3
import json
import urllib.parse
from io import StringIO

BODY_KEY = "Body"
RECORDS = 'Records'
S3_KEY = 's3'
BUCKET_KEY = 'bucket'
NAME = 'name'
KEY = 'key'
OBJECT_KEY = 'object'
DEFAULT_ENCODING = 'utf-8'
INPUT_KEY = 'input'
OUTPUT_KEY = 'output'
CONTENT_TYPE = 'ContentType'
GROUP_BY_KEY = "groupby"
AGG_KEY = 'agg'

s3 = boto3.client(S3_KEY)


def get_s3_response_from_event(event: dict) -> dict:
    """
    Refer to  `AWS docs <https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html>`_
    that reference a `snippet <https://serverlessland.com/snippets/integration-s3-to-lambda?utm_source=aws&utm_medium=link&utm_campaign=python&utm_id=docsamples&tab=python>`_

    :param event: the event json passed to a lambda as one of the two args; in an s3 trigger,
                  contains information about the s3 object that triggered
    :return: the Boto Response from the s3 client so you can read the "Body"

    """
    print(json.dumps(event, indent=4))
    # Get the object from the event and show its content type
    record_s3_data = event[RECORDS][0][S3_KEY]
    bucket = record_s3_data[BUCKET_KEY][NAME]
    key = urllib.parse.unquote_plus(record_s3_data[OBJECT_KEY][KEY], encoding=DEFAULT_ENCODING)
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print(f"Content type for {bucket}/{key} is {response.get(CONTENT_TYPE)}")
        return response
    except Exception as e:
        print(e)
        print(
            f'Error getting object {key} from bucket {bucket}. '
            'Make sure they exist and your bucket is in the same region as this function.'
        )
        raise e


def lambda_handler(event: dict, context):
    """
    The purpose of this lambda demo is to read a config JSON file as the event;
    it will contain the input data s3 info and the output s3 data.
    To make it somewhat more generalizable I'll allow the group by + agg to be configurable.

    In a more sophisticated pipeline, the options would be

    1. Have a more nuanced pipeline hard-coded into the lambda
    2. have a more sophisticated instruction parsing engine.

    For now, assume the triggering file contains something like the following:

    .. code-block:: json

        {
            "input": {
                "bucket": "jacobhickson-test",
                "key": "input/Online Retail.csv"
            },
            "output": {
                "bucket": "jacobhickson-test",
                "key": "output/agg_retail.csv"
            },
            "groupby": "Country",
            "agg": {
                "Quantity": [
                    "min",
                    "max"
                ]
            }
        }

    :param event: an s3 trigger event; assumed to be a .json file with further instructions.
    :param context: The default context information when the lambda is triggered. Unlikely to be
                    needed for my demo purposes.

    :return: Nothing returned to the caller; the outcome of this lambda is a file written to output.

    """
    response = get_s3_response_from_event(event=event)
    config_data = json.loads(response.get(BODY_KEY).read().decode())
    input_metadata = config_data.get(INPUT_KEY)
    output_metadata = config_data.get(OUTPUT_KEY)
    source_key = input_metadata.get(KEY)
    source_bucket = input_metadata.get(BUCKET_KEY)
    destination_key = output_metadata.get(KEY)
    destination_bucket = output_metadata.get(BUCKET_KEY)
    input_data = s3.get_object(Bucket=source_bucket, Key=source_key).get(BODY_KEY)
    data_frame = pd.read_csv(input_data)
    csv_buffer = StringIO()
    data_frame.groupby(config_data.get(GROUP_BY_KEY)).agg(config_data.get(AGG_KEY)).to_csv(
        csv_buffer
    )
    s3_resource = boto3.resource(S3_KEY)
    s3_resource.Object(destination_bucket, destination_key).put(Body=csv_buffer.getvalue())
    print(f"Wrote out to s3://{destination_bucket}/{destination_key}")
