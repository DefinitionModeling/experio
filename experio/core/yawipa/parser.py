"""Module for yawipa parser."""

import bz2
from pathlib import Path

from experio import const
from experio.console import console
from experio.core.yawipa import yawipa


class Parser(object):
    """Parse wiktionary dump with yawipa."""

    def __init__(self, base_path: str = const.BASE_PATH):
        """Initialize dataset object.

        Args:
            base_path (str): Base path of dataset.
        """
        self.base_path = base_path
        self.raw_path = '{0}.xml'.format(Path(self.base_path) / 'dump')
        self.dump_path = '{0}.bz2'.format(self.raw_path)
        self.parsed_path = '{0}.txt'.format(Path(self.base_path) / 'parsed')

        self.setup()

    def download(self) -> None:
        """Download wikitionary dump (english)."""
        yawipa.download('en', str(self.dump_path))

    def decompress(self) -> None:
        """Decompress wiktionary dump."""
        with bz2.open(self.dump_path, 'rb') as fin:
            with open(self.raw_path, 'wb') as fout:
                fout.write(fin.read())

    def parse(self) -> None:
        """Parse wiktionary dump."""
        yawipa.parse(str(self.raw_path), str(self.parsed_path))

    def setup(self) -> None:
        """Download necessary files."""
        if not Path(self.dump_path).is_file():
            console.log('Downloading wiktionary dump, please be patient...')
            self.download()

        if not Path(self.raw_path).is_file():
            console.log('Decompressing wiktionary dump...')
            self.decompress()

        if not Path(self.parsed_path).is_file():
            console.log('Parsing wiktionary dump...')
            self.parse()
