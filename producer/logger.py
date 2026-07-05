import logging

LOGGER_NAME = "DevPulse"

logger = logging.getLogger(LOGGER_NAME)

logger.setLevel(logging.INFO)

formatter = logging.Formatter(

    "%(asctime)s | %(levelname)s | %(message)s"

)

console = logging.StreamHandler()

console.setFormatter(formatter)

logger.addHandler(console)