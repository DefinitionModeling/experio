"""Experio main entrypoint."""

from rich import inspect

from experio.display import display
from experio.core.dataset.experio import EtymDefDataset


def main():
    """Run main program."""
    display()
    dataset = EtymDefDataset()
    inspect(dataset)


if __name__ == '__main__':
    main()
