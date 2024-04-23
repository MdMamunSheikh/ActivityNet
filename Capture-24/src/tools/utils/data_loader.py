import argparse
import re, os

def getMET(annotation: str)-> float: # returns MET score from the annotation text
  pattern = re.compile(r'MET\s+(\d+\.\d+)') 
  return float(re.findall(pattern, annotation)[0])

def getPID(fname: str)-> str: # returns PID  from a filepath i.e., 'P100'
  f = os.path.basename(fname)
  return re.compile(r'(P\d{3})').findall(f)[0]


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--datadir', '-d',default='data/', help="Directory containing the raw Capture-24 data. i.e., P001.csv.gz")
  parser.add_argument('--outdir', '-o',default='prepared_capture24', help="Directory for saving the captured24 processed data")
  parser.add_argument('--win_size', '-w', type=float, default=10, help='Define window size for each segment.')
  parser.add_argument('--FS', '-f', type=int, default=100, help='Define sampling frequency')
  parser.add_argument('--n_jobs', type=int, default=4, help='Number of jobs to load data')
  
  args = parser.parse_args()
  print(getMET('home activity;miscellaneous;walking;17150 walking household without observable loads;MET 2.0'))
  print(getPID('capture24/data/P001.csv.gz'))
