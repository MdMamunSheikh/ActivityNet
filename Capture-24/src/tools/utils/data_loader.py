import argparse


if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog="Pre-process Capture-24 Data")
  parser.add_argument('--datadir', '-d',default='data/', help="Directory containing the raw Capture-24 data. i.e., P001.csv.gz")
  parser.add_argument('--outdir', '-o',default='prepared_capture24', help="Directory for saving the captured24 processed data")
  parser.add_argument('--win_size', '-w', type=float, default=10, help='Define window size for each segment.')
  parser.add_argument('--FS', '-f', type=int, default=100, help='Define sampling frequency')
  parser.add_argument('--n_jobs', type=int, default=4, help='Number of jobs to load data')