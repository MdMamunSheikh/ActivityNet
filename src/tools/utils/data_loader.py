import pandas as pd
import numpy as np
import argparse
import os, re, sys
from joblib import Parallel, delayed
from glob import glob
from tqdm.notebook import tqdm

LABELING_STANDARD = ['label:WillettsSpecific2018']
ANN_PATH = 'annotation-label-dictionary.csv'
DATAFILES = 'P[0-9][0-9][0-9].csv.gz'

def main(args):
  os.system(f'mkdir -p {args.output_dir}')


def getMET(annotation: str)-> float: # returns MET score from the annotation text
  pattern = re.compile(r'MET\s+(\d+\.\d+)') # Pattern 'MET 1.5'
  return float(re.findall(pattern, annotation)[0]) # return MET score 1.5
def getPID(fname: str)-> str: # returns PID  from a filepath i.e., 'P100'
  f = os.path.basename(fname) # extract file name from path
  return re.compile(r'(P\d{3})').findall(f)[0] # return PID 'P100'


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_dir', '-d',default='data/', help="Directory containing the raw Capture-24 data. i.e., P001.csv.gz")
  parser.add_argument('--output_dir', '-o',default='prepared_capture24', help="Directory for saving the captured24 processed data")
  parser.add_argument('--win_size', '-w', type=float, default=10, help='Define window size for each segment.')
  parser.add_argument('--FS', '-f', type=int, default=100, help='Define sampling frequency')
  parser.add_argument('--n_jobs', type=int, default=4, help='Number of jobs to load data')
  
  args = parser.parse_args()
  print(getMET('home activity;miscellaneous;walking;17150 walking household without observable loads;MET 2.0'))
  print(getPID('capture24/data/P001.csv.gz'))
