import os
import numpy as np
import pandas as pd
from scipy import io
from tqdm import tqdm

#Helper Function
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

#1. List the MatLab files
mat_files = []
excludes = ['label.mat'] #Add files you want to exclude
for i in os.listdir():
    if i.split('.')[1] == 'mat' and i not in excludes:
        mat_files.append(i)

print(str(len(mat_files)) + " .mat files are going to be converted.")

index=1
files_count = len(mat_files)


#2. Iterating over the Files and Converting to CSV
for mat_file in mat_files:
    #print("Loading " + mat_file)
    mat = io.loadmat(mat_file)
    df = pd.DataFrame()
    base_name = 'djc_eeg'
    n = 15
    electrodes = 62

    #Prepare the Label Column
    base_label = np.array([ 1,  0, -1, -1,  0,  1, -1,  0,  1,  1,  0, -1,  0,  1, -1])
    labels = np.array([])
    for i in range(0, 15):
        labels = np.append(labels, np.ones(mat[base_name + str(i+1)][0].shape[0]) * base_label[i])

    #Set Data Columns based on Electrode Number
    for i in range(0, electrodes):
        electrode_data = np.array([])
        test = 0
        for j in range(0, n):
            electrode_data = np.append(electrode_data, mat[base_name + str(j+1)][i])
        df["E" + str(i+1)] = electrode_data
    df["label"] = labels
    print("Converting " + mat_file )
    
    chunksize = int(len(df) / 100) if len(df) >=100000 else len(df)
    
    #Setting up the ProgressBar for the CSV Convertion
    with tqdm(total=len(df)) as pbar:
        for i, cdf in enumerate(chunker(df, chunksize)):
            mode = "w" if i == 0 else "a"
            cdf.to_csv(mat_file.split('.')[0] + '.csv', index=False, header=True, mode=mode)
            pbar.update(chunksize)
    print( str(index) + " out of " + str(files_count) + " done.")
    index += 1


print("Finished.")
