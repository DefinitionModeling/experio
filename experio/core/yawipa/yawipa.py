"""Expose Yawipa library Yawipa code."""

from experio import const
from experio.jl import jl


def download(lang: str, output: str) -> None:
    """
    Download the Yawipa wiktionary dump.

    Args:
        lang (str): Language code (en/fr).
        output (str): Output directory.
    """
    jl.eval('Yawipa.download(\"{0}\", \"{1}\")'.format(lang, output))


def parse(
    dump: str,
    outfile: str,
    logfile: str = const.YAWIPA_LOG,
    edition: str = 'en',
) -> None:
    """
    Parse the Yawipa wiktionary dump.

    Args:
        dump (str): Path to (decompressed) wiktionary dump.
        outfile (str): Path to output file.
        logfile (str): Path to log file.
        edition (str): Language code (en/fr).
    """
    command = """
    Yawipa.parse(
        \"{0}\",
        \"{1}\",
        \"{2}\",
        \"{3}\",
        \".*:.*\",
        parsers=\"def,etym\",
    )
    """
    jl.eval(command.format(dump, edition, outfile, logfile))
