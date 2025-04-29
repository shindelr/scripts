#!/home/server/pi/homes/shindelr/scripts/pivpipe/.venv/bin/python3
"""
A script to run the Julia PIV portion of the pipeline.
"""

import os
import argparse
import subprocess
import logging
from multiprocessing import Pool
import yaml

logging.basicConfig(level=logging.INFO, format="%(asctime)s -- %(levelname)s -- %(message)s")
# NPROC = 61  # Num cores - 1 in Monarch?
NPROC = 4  # Num batches in test

def launch_batch(file, args):
    args.input = file  # Ensure procs each have their own in path
    args.output = os.path.join(os.path.abspath(args.output), os.path.basename(file))  # Ensure procs each have their own out dir
    if not os.path.isdir(args.output):
        os.mkdir(args.output)
    logging.info(f"Processing {args.input} -- Placing output in {args.output}")
    run_pipe(args=args)

def batches(abs_batch_dir):
    return [os.path.join(abs_batch_dir, f) for f in os.listdir(abs_batch_dir)]

def run_pipe(args):
    # Will probably need to be altered in future versions?
    exec_path = '/home/server/pi/homes/shindelr/Nearshore-PIV/piv_build/bin/PIVPipelineUtility'
    cmmd = [exec_path,
            str(args.N),
            str(args.crop_factor), 
            str(args.final_win_size), 
            str(args.ol), 
            args.output, 
            args.input, 
            str(args.verbosity)]
    subprocess.run(cmmd)

def get_args():
    output_mat_structure = """
This script will output the results of JuliaPIV as a .mat file with the following
structure:
    
x: [255x299 double]
y: [255x299 double]
pass_sizes: [3x2 double]
    overlap: 0.5
    method: 'multin'
        fn: {list of jpg files}
            u: [255x299 double]
            v: [255x299 double]
        npts: [255x299 double]  # number of data points that weren't NaN prior to time-average
        uStd: [255x299 double]  # standard deviation of the N results
        vStd: [255x299 double]  # ditto
"""

    parser = argparse.ArgumentParser(prog='PIV Pipeline Utility',
                                     description='Run Julia PIV on a batch of frames.',
                                     epilog=output_mat_structure)
    
    parser.add_argument('-N', 
                        help="The number of frames to average together at once.",
                        type=int)
                        # default=2)
    
    parser.add_argument('--crop_factor',
                        help='Gives a box to extract from the raw image. Should be a tuple of 4 ints wrapped in quotes.')
                        # default="24, 2425, 1, 2048")
    
    parser.add_argument('--final_win_size',
                        help='Final window size to evaluate PIV at.',
                        type=int)
                        # default=16)
    
    parser.add_argument('--ol', 
                        help='Window overlap for frame comparison.',
                        type=float)
                        # default=0.5)
    
    parser.add_argument('--output', '-o',
                        help='Where to output .mat files')
    
    parser.add_argument('--input', '-i',
                        help='Dir of .txt files containing image paths.')
    
    parser.add_argument('--verbosity', '-v',
                        help='1 for verbose print statements, 0 otherwise.',
                        type=int)
                        # default=0)
    parser.add_argument('--config', '-c', 
                        help='Load args from a config file')
    
    args = parser.parse_args()

    # Load the config file. Overrideable if desired!
    if args.config:
        with open(args.config, 'r') as f:
            try:
                config = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise e
        # Goes through the config file and checks if arg is already supplied via CL
        print(config)
        for key in config:
            print(key)
            if getattr(args, key) is None:
                attr = config[key]
                setattr(args, key, attr)
    
    return args



def main():
    args = get_args()
    txt_list = batches(args.input)
    logging.info(f"Found {len(txt_list)} .txt files\n")

    try:
        assert NPROC == len(txt_list), f"NPROC ({NPROC}) should ideally equal the number batches ({len(txt_list)}) to be processed." 
    except:
        if input("Proceed anyways? [y/n]   ") != 'y':
            return

    with Pool(processes=NPROC) as pool:
        pool.starmap(launch_batch, [(file, args) for file in txt_list])


if __name__ == '__main__':
    main()
