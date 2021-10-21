"""Expose pyjulia module."""

from pathlib import Path

from experio.console import console

try:
    from julia import Main
except Exception:
    import julia
    julia.install(quiet=True)
    from julia import Main


class Julia(object):
    """Class to manage julia calls."""

    def __init__(self):
        """Initialize Julia class."""
        self.julia = Main
        cwd = Path(__file__).parent

        console.log('Instantiating packages.')
        command = 'using Pkg; Pkg.activate("{0}"); Pkg.instantiate()'
        self.eval(command.format(cwd.parent))

        console.log('Loading julia module.')
        self.eval('include(\"{0}\")'.format(cwd / 'experio.jl'))

    def eval(self, code: str):
        """Evaluate code in julia.

        Args:
            code (str): Code to evaluate.
        """
        console.log('Evaluating julia: {0}'.format(code))
        self.julia.eval(code)


# expose julia object to other modules
jl = Julia()
