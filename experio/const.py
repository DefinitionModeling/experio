"""Module for constants."""

from pathlib import Path

# data
BASE_PATH = 'data'

# logs
LOG_PATH = 'logs'
YAWIPA_LOG = '{0}/yawipa.log'.format(LOG_PATH)

# urls
YAWIPA_URL = 'https://www.cs.jhu.edu/~winston/yawipa-data'


# make paths if they don't exist
Path(BASE_PATH).mkdir(parents=True, exist_ok=True)
Path(LOG_PATH).mkdir(parents=True, exist_ok=True)
