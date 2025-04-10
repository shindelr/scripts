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
def cli(indir, files_per, out_dir):
    """
    A script to partition a directory of files into many directories with the OG
    files split between them. 
    """
    abs_in = os.path.abspath(indir)
    abs_out = os.path.abspath(out_dir)
    out_dir_setup(abs_out)

def out_dir_setup(abs_out: str) -> None:
    """
    Ensure the out directory exists, creates it if it doesn't.
    """
    if not os.path.isdir(abs_out):
        print(f"Building a directory at {abs_out}")
        os.makedirs(abs_out)
    return
