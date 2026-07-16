from github_client import GitHubClient
from transformer import EventTransformer
from aws_client import AWSClient

github = GitHubClient()

transformer = EventTransformer()

aws = AWSClient()

events = github.fetch_events()

events = transformer.transform(events)

aws.send_events(events)