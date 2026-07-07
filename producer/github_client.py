"""
github_client.py

Responsible for communicating with the GitHub Events API.
"""

import time
import requests

from config import (
    GITHUB_API,
    HEADERS,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY
)

from logger import logger


class GitHubClient:

    def __init__(self):
        self.last_etag = None

    def fetch_events(self):
        """
        Fetch latest GitHub public events.
        Returns:
            list : Raw GitHub Events
        """

        headers = HEADERS.copy()

        # GitHub conditional request
        if self.last_etag:
            headers["If-None-Match"] = self.last_etag

        for attempt in range(MAX_RETRIES):

            try:

                response = requests.get(
                    GITHUB_API,
                    headers=headers,
                    timeout=REQUEST_TIMEOUT
                )

                # Nothing new
                if response.status_code == 304:

                    logger.info("No new events.")

                    return []

                response.raise_for_status()

                # Save ETag
                self.last_etag = response.headers.get("ETag")

                events = response.json()

                logger.info(
                    f"Fetched {len(events)} events."
                )

                return events

            except requests.exceptions.RequestException as e:

                logger.warning(
                    f"GitHub request failed "
                    f"(Attempt {attempt+1}/{MAX_RETRIES}) : {e}"
                )

                time.sleep(RETRY_DELAY)

        logger.error("GitHub API unavailable.")

        return []