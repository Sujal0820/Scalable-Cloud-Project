"""
DevPulse Project Constants
"""

# --------------------------
# Project Information
# --------------------------

PROJECT_NAME = "DevPulse"

VERSION = "2.0"

SOURCE = "GitHub Public Events"

# --------------------------
# Event Categories
# --------------------------

EVENT_CATEGORIES = {

    "PushEvent": "Development",

    "CreateEvent": "Repository",

    "ForkEvent": "Community",

    "WatchEvent": "Community",

    "PullRequestEvent": "Collaboration",

    "ReleaseEvent": "Release"

}

# --------------------------
# Valid Repository Events
# --------------------------

VALID_EVENTS = list(EVENT_CATEGORIES.keys())