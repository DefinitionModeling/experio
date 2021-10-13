"""Module for dataset object."""

from pathlib import Path
from urllib.request import urlretrieve

from experio.console import console


class Dataset(object):
    """Text-based dataset object."""

    name: str
    url: str
    base_path: str

    def __init__(self, name: str, url: str, base_path: str = 'data/'):
        """Initialize dataset object.

        Args:
            name (str): Name of dataset.
            url (str): URL of dataset.
            base_path (str): Base path of dataset.
        """
        self.name = name
        self.url = url
        self.base_path = base_path
        self.file_path = '{0}.text'.format(Path(self.base_path) / self.name)

        # make base path if it doesn't exist
        Path(self.base_path).mkdir(parents=True, exist_ok=True)
        self.raw = self.load()

    def download(self):
        """Download dataset."""
        console.log('Downloading {0}'.format(self.url))
        urlretrieve(self.url, self.file_path)

    def load(self) -> str:
        """Load dataset.

        Returns:
            str: Dataset content.
        """
        if not Path(self.file_path).is_file():
            console.log('Dataset not found.')
            self.download()

        with open(self.file_path, 'r') as fi:
            console.log('Opening {0}...'.format(self.file_path))
            return fi.read()
