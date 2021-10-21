"""Module for printing to the terminal."""

from experio.console import console


def print_logo():
    """Print the logo to the terminal."""
    logo = [
        '=======',
        'experio',
        '=======',
    ]

    for line in logo:
        console.log(line)


def display():
    """Display the logo and the help message."""
    print_logo()
