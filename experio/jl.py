"""Expose pyjulia module."""

from pathlib import Path

from experio.console import console

try:
    from julia import Main as jl
except Exception:
    import julia
    julia.install(quiet=True)
    from julia import Main as jl

# instantiate packages
jl.eval('using Pkg; Pkg.instantiate()')

try:
    jl.imported()
except AttributeError:
    console.log('Loading julia module.')
    # load exposed julia functions
    cwd = Path(__file__).parent
    jl.eval('include(\"{0}\")'.format(cwd / 'experio.jl'))
    jl.imported()
