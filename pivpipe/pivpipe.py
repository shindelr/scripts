#!/home/server/pi/homes/shindelr/scripts/pivpipe/.venv/bin/python3
"""
A script to run the Julia PIV portion of the pipeline.
"""

import os
import subprocess
import logging
from multiprocessing import Pool
import yaml
import click
from copy import deepcopy

logging.basicConfig(level=logging.INFO, format="%(asctime)s -- %(levelname)s -- %(message)s")
# NPROC = 61  # Num cores - 1 in Monarch?

def launch_batch(file, args):
    """
    Make copies of arguments to avoid race conditions while multi-processing. 
    Each proc gets its own output directory (like batch1 batch2... batchn), this
    way the processes are not competing for I/O to the same region of memory.
    """
    local_args = deepcopy(args)
    local_args["input"] = file  # Ensure procs each have their own in path
    local_args["output"] = os.path.join(os.path.abspath(local_args["output"]), os.path.basename(file))  # Ensure procs each have their own out dir
    local_args["output"] = local_args["output"].removesuffix(".txt")
    
    if not os.path.isdir(local_args["output"]):
        os.mkdir(local_args["output"])
    run_pipe(args=local_args)

def batches(abs_batch_dir):
    """
    Do path magic. TODO: This is a bad doc string!
    """
    return [os.path.join(abs_batch_dir, f) for f in os.listdir(abs_batch_dir)]

def run_pipe(args):
    """
    Run the julia binary for PIV. 
    """
    # Will probably need to be altered in future versions?
    exec_path = '/home/server/pi/homes/shindelr/Nearshore-PIV/piv_build/bin/PIVPipelineUtility'
    cmmd = [
        exec_path,
        str(args["N"]),
        str(args["crop_factor"]),
        str(args["final_win_size"]),
        str(args["ol"]),
        args["output"],
        args["input"],
        str(args["quiet"]),
        str(args["downsample_factor"]),
        str(args["save_images"]).lower()
    ]
    subprocess.run(cmmd, check=True)

def load_config(config_path, cli_args):
    """
    Load the configuration YAML file for this PIV run. 
    """
    # Load the config file. Overrideable if desired!
    with open(config_path, 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise e
    # Goes through the config file and checks if arg is already supplied via CL
    for key, value in config.items():
        if cli_args.get(key) is None:
            cli_args[key] = value
    
    return cli_args

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-N', type=int, help="Number of frames to average together.")
@click.option('--crop_factor', '-r', help="Crop box as a quoted string of 4 ints.")
@click.option('--final_win_size', '-w', type=int, help="Final window size.")
@click.option('--ol', type=float, help="Window overlap.")
@click.option('--output', '-o', help="Output directory for .mat files.")
@click.option('--input', '-i', help="Directory of .txt files.")
@click.option('--quiet', '-q', is_flag=True, help="Quiet mode.")
@click.option('--config', '-c', type=click.Path(exists=True), help="YAML config file to load defaults.")
@click.option('-d', '--downsample_factor', type=int, help="Image downsampling factor.")
@click.option('-p', '--NPROC', type=int, help='Number of processes to use. Ideally should equal the number of batches if possible.')
@click.option('-s', '--save_images', is_flag=True, help="Save cropped and downsampled images. Note that extra I/O slows execution.")
def main(**kwargs):
    logging.info("Running PIV")
    if kwargs.get("config"):
        kwargs = load_config(kwargs["config"], kwargs)
    if kwargs['quiet']:
        kwargs['quiet'] = 0
    else:
        kwargs['quiet'] = 1

    txt_list = batches(kwargs["input"])
    logging.info(f"Found {len(txt_list)} .txt files\n")

    try:
        assert kwargs['NPROC'] == len(txt_list)
    except:
        print(f"NPROC ({kwargs['NPROC']}) should ideally equal the number batches ({len(txt_list)}) to be processed.")
        if input("Proceed anyways? [y/n] ") != 'y':
            return

    with Pool(processes=kwargs['NPROC']) as pool:
        pool.starmap(launch_batch, [(file, kwargs) for file in txt_list])

    print("\n")
    logging.info("Cleaning up file structure.")
    out_dirs = os.listdir(kwargs["output"])
    for dir in out_dirs:
        try:
            files = os.listdir(os.path.join(kwargs["output"], dir))
            files_src = [os.path.join(kwargs["output"], dir, f) for f in files]
            files_dst = [os.path.join(kwargs["output"], f) for f in files]
            for i in range(len(files_src)):
                os.rename(files_src[i], files_dst[i])
            os.rmdir(os.path.join(kwargs["output"], dir))
        except NotADirectoryError:
            exception_path = os.path.join(kwargs["output"], dir)
            logging.warning(f"Skipping existing non-directory file: {exception_path}")

    logging.info("Job Completed.")

if __name__ == '__main__':
    main()
