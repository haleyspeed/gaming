import os
import csv
import numpy as np
import glob
import pandas as pd

def concat (dir_in):
    df = pd.DataFrame()
    orig_dir = os.getcwd()
    os.chdir (dir_in)
    i = 1
    for f in glob.glob('*{}'.format('csv')):
        #print(i,f)
        df = df.append(pd.read_csv(f,dtype='unicode'))
        df = df.drop_duplicates()
    df.to_csv(os.path.join('concatenated.csv'))
    os.chdir(orig_dir)
    return df
