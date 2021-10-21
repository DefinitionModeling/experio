"""Experio main entrypoint."""

from experio.console import console
from experio.dataset import EtymDefDataset
from experio.display import display


def main():
    """Run main program."""
    display()
    ds = EtymDefDataset()
    console.log(ds.dataset())


if __name__ == '__main__':
    main()
