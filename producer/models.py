from dataclasses import dataclass

@dataclass
class GitHubEvent:

    event_id: str

    event_type: str

    category: str

    repository_owner: str

    repository_name: str

    repository_full_name: str

    actor: str

    github_timestamp: str

    ingested_timestamp: str

    source: str

    producer_version: str

    year: int

    month: int

    day: int

    hour: int