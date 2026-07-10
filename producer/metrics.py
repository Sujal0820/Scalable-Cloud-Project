"""
metrics.py

Collects runtime metrics for benchmarking.
"""

import time

from logger import logger


class ProducerMetrics:

    def __init__(self):

        self.start_time = time.time()

        self.poll_count = 0

        self.total_raw_events = 0

        self.total_valid_events = 0

        self.total_sent_events = 0

    def poll_started(self):

        self.poll_start = time.time()

    def poll_finished(self):

        elapsed = time.time() - self.poll_start

        self.poll_count += 1

        logger.info(
            f"Poll #{self.poll_count} completed in "
            f"{elapsed:.2f} sec"
        )

    def add_raw_events(self, count):

        self.total_raw_events += count

    def add_valid_events(self, count):

        self.total_valid_events += count

    def add_sent_events(self, count):

        self.total_sent_events += count

    def summary(self):

        runtime = time.time() - self.start_time

        throughput = 0

        if runtime > 0:
            throughput = self.total_sent_events / runtime

        logger.info("=" * 60)

        logger.info("Producer Metrics")

        logger.info("=" * 60)

        logger.info(f"Runtime              : {runtime:.2f} sec")

        logger.info(f"Polls Completed      : {self.poll_count}")

        logger.info(f"Raw Events           : {self.total_raw_events}")

        logger.info(f"Valid Events         : {self.total_valid_events}")

        logger.info(f"Sent To Kinesis      : {self.total_sent_events}")

        logger.info(f"Throughput           : {throughput:.2f} events/sec")

        logger.info("=" * 60)