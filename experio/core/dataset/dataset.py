"""Module for dataset object."""

from pathlib import Path
from typing import Optional
from urllib.request import urlretrieve

from tqdm import tqdm

from experio import const
from experio.console import console
from experio.core.dataset.download import report_hook


class Dataset(object):
    """Text-based dataset object."""

    name: str
    url: str
    base_path: str

    def __init__(
        self,
        name: str,
        url: str,
        base_path: Optional[str] = const.BASE_PATH,
    ):
        """Initialize dataset object.

        Args:
            name (str): Name of dataset.
            url (str): URL of dataset.
            base_path (Optional[str]): Base path of the dataset.
        """
        self.name = name
        self.url = url
        self.base_path = base_path
        self.file_path = '{0}.txt'.format(Path(self.base_path) / self.name)

        # download text file
        if not Path(self.file_path).is_file():
            console.log('Dataset not found.')
            self.download()

    def download(self) -> None:
        """Download dataset."""
        console.log(
            'Downloading "{0}" to {1}.'.format(self.url, self.file_path),
        )
        # progress bar
        with tqdm(
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            miniters=1,
            desc=self.file_path,
        ) as tq:
            urlretrieve(
                self.url,
                filename=self.file_path,
                reporthook=report_hook(tq),
                data=None,
            )
