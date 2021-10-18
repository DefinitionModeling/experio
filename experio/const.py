"""Module for constants."""

from pathlib import Path

# data
BASE_PATH = 'data'

# logs
LOG_PATH = 'logs'
YAWIPA_LOG = '{0}/yawipa.log'.format(LOG_PATH)

# make paths if they don't exist
Path(BASE_PATH).mkdir(parents=True, exist_ok=True)
Path(LOG_PATH).mkdir(parents=True, exist_ok=True)
