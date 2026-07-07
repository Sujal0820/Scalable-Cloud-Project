"""
producer.py

Main Producer Application
"""

import time

from config import POLL_INTERVAL

from github_client import GitHubClient
from transformer import EventTransformer
from aws_client import AWSClient
from metrics import ProducerMetrics

from logger import logger


def main():

    github = GitHubClient()

    transformer = EventTransformer()

    aws = AWSClient()

    metrics = ProducerMetrics()

    logger.info("=" * 60)
    logger.info("DevPulse Producer Started")
    logger.info("=" * 60)

    try:

        while True:

            metrics.poll_started()

            # ----------------------------------
            # Fetch Raw Events
            # ----------------------------------

            raw_events = github.fetch_events()

            metrics.add_raw_events(len(raw_events))

            if not raw_events:

                metrics.poll_finished()

                time.sleep(POLL_INTERVAL)

                continue

            # ----------------------------------
            # Transform Events
            # ----------------------------------

            valid_events = transformer.transform(raw_events)

            metrics.add_valid_events(len(valid_events))

            if valid_events:

                # ------------------------------
                # Send to Kinesis
                # ------------------------------

                aws.send_events(valid_events)

                metrics.add_sent_events(len(valid_events))

            metrics.poll_finished()

            metrics.summary()

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:

        logger.info("Stopping Producer...")

        metrics.summary()

    except Exception as e:

        logger.exception(e)


if __name__ == "__main__":

    main()