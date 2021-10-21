"""Wiktionary datasets from experio."""

from experio.core.dataset.yawipa import DefinitionDataset, EtymologyDataset
from experio.jl import jl


class EtymDefDataset(object):
    """Dataset with Etymologies and Definitions."""

    def __init__(self):
        """Initialize the dataset."""
        super().__init__()

        # initialize datasets
        EtymologyDataset()
        DefinitionDataset()

        # load data

    def load(self):
        """Load the dataset."""
