import os

# ------------------------------------
# GitHub
# ------------------------------------

GITHUB_TOKEN = "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"

GITHUB_API = "https://api.github.com/events"

POLL_INTERVAL = 5

REQUEST_TIMEOUT = 20

HEADERS = {

    "Authorization": f"Bearer {GITHUB_TOKEN}",

    "Accept": "application/vnd.github+json",

    "User-Agent": "DevPulse"

}

# ------------------------------------
# AWS
# ------------------------------------

AWS_REGION = "us-east-1"

S3_BUCKET = "devpulse-github-data-2026"

KINESIS_STREAM = "devpulse-event-stream"

# ------------------------------------
# Producer
# ------------------------------------

S3_BATCH_SIZE = 50

MAX_RETRIES = 3

RETRY_DELAY = 3