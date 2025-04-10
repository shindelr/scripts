#!/usr/bin/env python3
"""
Author: Robin Shindelman
Date: 2025-04-09
A script to partition a directory of files into many directories with the OG
files split between them. This script was originally built to facilitate the
OSU ROXSI SVS pipeline.
"""

import os, click, shutil

@click.command()
@click.argument('indir')
@click.option('-n', '--files-per', type=int, default=6)
@click.option('-o', '--out-dir', type=str, default='.')
@click.option('-ow', '--overwrite', type=bool, default=False)
def cli(indir, files_per, out_dir, overwrite):
    """
    A script to partition a directory of files into many directories with the OG
    files split between them. 
    """
    abs_in = os.path.abspath(indir)
    abs_out = os.path.abspath(out_dir)
    out_dir_setup(abs_out, overwrite)

def out_dir_setup(abs_out: str, overwite: bool) -> None:
    """
    Ensure the out directory exists, creates it if it doesn't. If the overwrite
    flag is set, all items in the directory will be emptied before the new .txt
    files are written.
    """
    if not os.path.isdir(abs_out):
        print(f"Building a directory at {abs_out}")
        os.makedirs(abs_out)
    elif os.path.isdir(abs_out) and overwite:
        confirm = input(f"Overwriting {abs_out}\n Correct? [y/n]  ")
        if confirm == 'y':
            shutil.rmtree(abs_out)
            os.mkdir(abs_out)

        return

    return
