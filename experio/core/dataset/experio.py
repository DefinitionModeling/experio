"""Wiktionary datasets from experio."""

from pathlib import Path
from typing import Optional

import pandas as pd
import pyarrow as pa

from experio import const
from experio.console import console
from experio.core.dataset.yawipa import DefinitionDataset, EtymologyDataset
from experio.jl import jl


class EtymDefDataset(object):
    """Dataset with Etymologies and Definitions."""

    name: str
    file_path: str

    def __init__(self, base_path: Optional[str] = const.BASE_PATH):
        """Initialize the dataset.

        Args:
            base_path (Optional[str]): Base path of the dataset. Defaults to
                const.BASE_PATH.
        """
        self.name = 'final'
        self.base_path = base_path
        self.file_path = '{0}.arrow'.format(Path(self.base_path) / self.name)

        # initialize base datasets
        EtymologyDataset()
        DefinitionDataset()

        # create arrow file datasets
        if not Path(self.file_path).is_file():
            console.log('Dataset not found.')
            self.load()

    def load(self):
        """Load the dataset."""
        jl.eval('load_dataset()')

    def dataset(self) -> pd.DataFrame:
        """Get the dataset.

        Returns:
            pd.DataFrame: The dataset as pandas dataframe.
        """
        reader = pa.ipc.open_file(self.file_path)
        return reader.read_all().to_pandas()
