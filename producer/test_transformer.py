from github_client import GitHubClient
from transformer import EventTransformer

github = GitHubClient()
transformer = EventTransformer()

raw = github.fetch_events()

events = transformer.transform(raw)

print(f"Total transformed events: {len(events)}")

if events:
    print(events[0])