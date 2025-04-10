"""
Author: Robin Shindelman
Date: 2025-04-10

Move the most recently downloaded file or directory from the downloads to a
directory of your choosing.
"""

import os, click

@click.command()
@click.option('-o', '--out-dir', type=str, default='.')
def cli(out_dir: str):
    """
    Move the most recently downloaded file or directory from the downloads to a
    directory of your choosing.
    """
    click.echo("Hey there")
