"""Experio main entrypoint."""

from rich import inspect

from experio.console import console
from experio.dataset import DefinitionDataset, EtymologyDataset


def main():
    """Run main program."""
    console.log('Experio')

    def_data = DefinitionDataset()
    console.log(len(def_data.raw))

    etym_data = EtymologyDataset()
    console.log(len(etym_data.raw))


if __name__ == '__main__':
    main()
