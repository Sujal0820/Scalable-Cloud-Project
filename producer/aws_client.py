"""
aws_client.py

Handles communication with Amazon Kinesis.
"""

import json
import boto3

from botocore.exceptions import ClientError

from config import (
    AWS_REGION,
    KINESIS_STREAM
)

from logger import logger


class AWSClient:

    def __init__(self):

        self.kinesis = boto3.client(
            "kinesis",
            region_name=AWS_REGION
        )

    def send_events(self, events):

        if not events:
            return

        records = []

        for event in events:

            records.append(
                {
                    "Data": json.dumps(event),
                    "PartitionKey": event["repository"]["owner"]
                }
            )

        try:

            response = self.kinesis.put_records(
                StreamName=KINESIS_STREAM,
                Records=records
            )

            failed = response["FailedRecordCount"]

            success = len(records) - failed

            logger.info(
                f"Kinesis -> Success: {success} | Failed: {failed}"
            )

            if failed > 0:

                for index, record in enumerate(response["Records"]):

                    if "ErrorCode" in record:

                        logger.warning(
                            f"Record {index} failed : "
                            f"{record['ErrorCode']} "
                            f"{record['ErrorMessage']}"
                        )

        except ClientError as e:

            logger.error(f"Kinesis Error : {e}")

        except Exception as e:

            logger.error(f"Unexpected Error : {e}")