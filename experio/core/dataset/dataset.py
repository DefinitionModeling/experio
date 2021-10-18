"""Module for dataset object."""

from pathlib import Path
from urllib.request import urlretrieve

from experio import const
from experio.console import console


class Dataset(object):
    """Text-based dataset object."""

    name: str
    url: str
    base_path: str

    def __init__(self, name: str, url: str, base_path: str = const.BASE_PATH):
        """Initialize dataset object.

        Args:
            name (str): Name of dataset.
            url (str): URL of dataset.
            base_path (str): Base path of dataset.
        """
        self.name = name
        self.url = url
        self.base_path = base_path
        self.file_path = '{0}.txt'.format(Path(self.base_path) / self.name)

        self.raw = self.load()

    def download(self) -> None:
        """Download dataset."""
        console.log('Downloading {0}'.format(self.url))
        urlretrieve(self.url, self.file_path)

    def load(self) -> None:
        """Load dataset."""
        if not Path(self.file_path).is_file():
            console.log('Dataset not found.')
            self.download()
