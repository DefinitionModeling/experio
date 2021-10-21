"""Module for downloading and extracting data-files from the internet."""

from tqdm import tqdm


def report_hook(instance: tqdm):
    """Wrap tqdm instance.

    Args:
        instance(tqdm): tqdm instance.

    Returns:
        update_to: updated progress bar.
    """
    last_b = [0]

    def update_to(blocks: int = 1, bsize: int = 1, tsize: int = None):
        """Update the progress bar.

        Args:
            blocks(int): Number of blocks transferred so far.
            bsize(int): Size of each block (in tqdm units).
            tsize(int): Total size (in tqdm units).
        """
        if tsize is not None:
            instance.total = tsize
        instance.update((blocks - last_b[0]) * bsize)
        last_b[0] = blocks

    return update_to
