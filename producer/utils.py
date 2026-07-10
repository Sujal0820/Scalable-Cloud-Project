from datetime import datetime


def utc_now():

    return datetime.utcnow()


def utc_string():

    return utc_now().strftime(

        "%Y-%m-%dT%H:%M:%SZ"

    )


def split_repository(full_name):

    owner, repo = full_name.split("/")

    return owner, repo


def time_parts():

    now = utc_now()

    return (

        now.year,

        now.month,

        now.day,

        now.hour

    )