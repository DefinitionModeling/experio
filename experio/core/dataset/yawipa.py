"""Wiktionary datasets from yawipa."""

from experio import const
from experio.core.dataset.dataset import Dataset


class DefinitionDataset(Dataset):
    """Wikitionary definitions dataset."""

    def __init__(self):
        """Initialize dataset."""
        name = 'def'
        super().__init__(
            name=name,
            url='{0}/{1}'.format(const.YAWIPA_URL, name),
        )


class EtymologyDataset(Dataset):
    """Wikitionary etymologies dataset."""

    def __init__(self):
        """Initialize dataset."""
        name = 'etym'
        super().__init__(
            name=name,
            url='{0}/{1}'.format(const.YAWIPA_URL, name),
        )
