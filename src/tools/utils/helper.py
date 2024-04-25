import re, os

def getMET(annotation: str)-> float: # returns MET score from the annotation text
  pattern = re.compile(r'MET\s+(\d+\.\d+)') # Pattern 'MET 1.5'
  return float(re.findall(pattern, annotation)[0]) # return MET score 1.5


def getPID(fname: str)-> str: # returns PID  from a filepath i.e., 'P100'
  f = os.path.basename(fname) # extract file name from path
  return int(re.compile(r'P(\d{3})').findall(f)[0]) # return PID 'P100'


def genLabel(label, col_name, df) -> tuple:
  map = dict(zip(label.index, label[col_name]))
  df[col_name] = df.annotation.map(map)
  uniq = set(map.values())
  try:
    map = {'standing': 0, 'sitting': 1, 'vehicle': 2, 'mixed-activity': 3, 'bicycling': 4, 'sports': 5, 'sleep': 6, 'manual-work': 7, 'walking': 8, 'household-chores': 9}
    df[col_name] = df[col_name].map(map)
  except:
    map = dict(zip(uniq, range(len(uniq))))
    df[col_name] = df[col_name].map(map)
  
  # print(map)
  return map, df
