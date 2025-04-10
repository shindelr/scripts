"""
Author: Robin Shindelman
Date: 2025-04-10

Move the most recently downloaded file or directory from the downloads to a
directory of your choosing.
"""

import os, click, shutil

@click.command()
@click.option('-o', '--out-dir', type=str, default='.')
def cli(out_dir: str):
    """
    Move the most recently downloaded file or directory from the downloads to a
    directory of your choosing.
    """
    file = get_recent_dl()
    click.echo(f"{file} --> {out_dir}")
    shutil.move(file, out_dir)

def get_recent_dl() -> str:
    """Get path to most recent download."""
    dl_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    if os.path.isdir(dl_dir):
        files = [
            os.path.join(dl_dir, f) for f in os.listdir(dl_dir)
            if os.path.isfile(os.path.join(dl_dir, f))
        ]
        file = max(files, key=os.path.getctime)
        return file
    else:
        raise NotADirectoryError