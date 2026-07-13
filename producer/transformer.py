"""
transformer.py

Transforms raw GitHub events into the
DevPulse standard schema.
"""

from constants import EVENT_CATEGORIES
from logger import logger
from utils import utc_string


class EventTransformer:

    def __init__(self):
        self.seen_events = set()

    def transform(self, raw_events):

        transformed_events = []

        for event in raw_events:

            try:

                event_id = event.get("id")

                # Ignore duplicates
                if event_id in self.seen_events:
                    continue

                self.seen_events.add(event_id)

                event_type = event.get("type")

                # Ignore unsupported events
                if event_type not in EVENT_CATEGORIES:
                    continue

                # --------------------------
                # Handle CreateEvent
                # Keep ONLY repository creation
                # --------------------------

                if event_type == "CreateEvent":

                    payload = event.get("payload", {})

                    if payload.get("ref_type") != "repository":
                        continue

                repo = event.get("repo", {}).get("name", "")

                if "/" in repo:
                    owner, repository = repo.split("/", 1)
                else:
                    owner = "unknown"
                    repository = repo

                transformed_event = {

                    # -----------------------
                    # Event Information
                    # -----------------------

                    "event_id": event_id,

                    "event_type": event_type,

                    "category": EVENT_CATEGORIES[event_type],

                    # -----------------------
                    # Repository
                    # -----------------------

                    "repository": {

                        "owner": owner,

                        "name": repository,

                        "full_name": repo
                    },

                    # -----------------------
                    # Actor
                    # -----------------------

                    "actor": {

                        "username":
                            event.get("actor", {}).get("login", "unknown")
                    },

                    # -----------------------
                    # Time
                    # -----------------------

                    "timestamps": {

                        "github":
                            event.get("created_at"),

                        "ingested":
                            utc_string()
                    },

                    # -----------------------
                    # Metadata
                    # -----------------------

                    "metadata": {

                        "source":
                            "GitHub",

                        "version":
                            "2.0"
                    }

                }

                transformed_events.append(
                    transformed_event
                )

            except Exception as e:

                logger.warning(
                    f"Skipped malformed event : {e}"
                )

        logger.info(
            f"Valid Events : {len(transformed_events)}"
        )

        return transformed_events