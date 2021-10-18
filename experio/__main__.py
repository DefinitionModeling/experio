"""Experio main entrypoint."""

from rich import inspect

from experio.console import console
from experio.dataset import DefinitionDataset, EtymologyDataset


def main():
    """Run main program."""
    console.log('Experio')

    DefinitionDataset()
    EtymologyDataset()


if __name__ == '__main__':
    main()
