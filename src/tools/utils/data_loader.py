from types import NoneType
import pandas as pd
import numpy as np
import argparse
import os, re, sys
from joblib import Parallel, delayed
from glob import glob
from tqdm.notebook import tqdm
from IPython.display import display
from helper import getMET, getPID, genLabel

LABELING_STANDARD = ['label:WillettsSpecific2018']
ANN_PATH = 'annotation-label-dictionary.csv'
DATAFILES = 'P[0-9][0-9][0-9].csv.gz'

def main(args):
  os.system(f'mkdir -p {args.output_dir}')
  outputs = []
  files = glob(os.path.join(args.data_dir, DATAFILES))
  files.sort()
  counter = 0
  # print(files)
  for f in tqdm(files):
    counter +=1
    df = read(fpath= f, label_path= os.path.join(args.data_dir, ANN_PATH), FS=args.fs, standard=args.standard, args=args)
    print('Completed..........') if args.verbose else None
    outputs.append(df)
    if counter%args.save_freq ==0 or counter==len(files):
      data = pd.concat(outputs, ignore_index=True)
      data.to_pickle(os.path.join(args.output_dir, f'prcessed_data_{counter}.pkl'), compression='gzip')
      outputs = []
      print(f'<<<<< Saving processed_{counter}.pkl >>>>>')
  print(df.head())


def read(fpath: str, label_path: str, FS=100, standard: str = 'label:WillettsSpecific2018', args=None):
  pid = getPID(fpath)
  if args.verbose:
    display(f'P{pid} Loading..........')
  data = pd.read_csv(fpath, index_col='time', parse_dates=['time'], dtype={
      'x':'f', 'y':'f', 'x':'f', 'annotation':'str'
  })
  label = pd.read_csv(label_path, index_col='annotation', dtype='string')
  if args.verbose:
    display(f'\tDataframe dimesion: {data.shape} \n\tFiltering...')
  label_dict, data = genLabel(label, args.standard, data)
  data['pid'] = pid
    #filter NAN values
  data.dropna(inplace=True)
  data['MET'] = data.annotation.apply(getMET)
  # split the data if there are time gap of 1s in each consecutive datapoints
  time_diff = data.index.to_series().diff().dt.total_seconds()
  gap = 1
  groups = (time_diff>gap).cumsum()
  resampled_data = []
  display('\tSegmenting...') if args.verbose else None
  for _,seg in (data.groupby(groups)):
    seg = seg.resample(f'{(1/FS)*1000}ms')
    resampled_data.append(
        seg.interpolate(method='linear').fillna('backfill')
        )
  assert data.isna().sum().sum()==0, "dataset contain NAN values. Please check it again."
  data = pd.concat(resampled_data)
  data.reset_index(drop=True, inplace=True)
  # data.drop(columns=['annotation'], inplace=True)
  dtypes = {'x':'f2', 'y':'f2', 'z': 'f2', 'annotation':'str', args.standard:'i1', 'pid':'i1', 'MET':'f4'}

  # fill missing numerical value using linear interpolation and categorical value by backfill method
  return data.astype(dtypes)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_dir', '-d',default='data/', help="Directory containing the raw Capture-24 data. i.e., P001.csv.gz")
  parser.add_argument('--output_dir', '-o',default='prepared_capture24', help="Directory for saving the captured24 processed data")
  parser.add_argument('--win_size', '-w', type=float, default=10, help='Define window size for each segment.')
  parser.add_argument('--fs', '-f', type=int, default=100, help='Define sampling frequency')
  parser.add_argument('--n_jobs', type=int, default=4, help='Number of jobs to load data')
  parser.add_argument('--standard', default='label:WillettsSpecific2018', help='Labeliing mapping column name')
  parser.add_argument("--verbose", '-v', action="store_true", help="increase output verbosity") 
  parser.add_argument("--save_freq", '-s', type=int, default=1, help='saving freuquency of the output files')
  
  args = parser.parse_args()
  main(args)
  # print(getMET('home activity;miscellaneous;walking;17150 walking household without observable loads;MET 2.0'))
  # print(getPID('capture24/data/P001.csv.gz'))
