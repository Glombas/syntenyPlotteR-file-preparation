#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Oct 24, 2024

@author: glombik
"""
import glob
import numpy as np
import pandas as pd

#create a list for files in folder
read_files = []
#put all the alignment files in a list
for file in glob.glob('/Users/glombik/Library/CloudStorage/OneDrive-NorwichBioscienceInstitutes/morris_lab/assembly_qc/synteny_analysis/brapa/rt_ro18/' + 'filtered*.txt',recursive=True):
    read_files.append(file)

#run the whole transformation in a loop on all files
for fread in read_files:
   #empty data list before opening each file
    data = []
    with open(fread, 'r') as file:
        next(file)
        for line in file:
        # Split the line by spaces (handling multiple spaces)
            data.append(line.split())
    #transform it into a data frame
    map_example = pd.DataFrame(data)
    #replace empty fields labelled 'None' to NA
    map_example.replace('None', np.nan, inplace=True)
    
    #filter out rows with NAs starting in the second column
    map_example_filt = map_example[map_example.iloc[:, 1:].notna().sum(axis=1) > 0]
    
    #add the sequence alignment label to a new column and then to each respective row
    mask = map_example_filt[0].str.startswith('>')

    map_example_filt.loc[mask, 'concatenated'] = map_example_filt.loc[mask, [0,1]].apply(lambda row: ' '.join(row.astype(str)), axis=1)

    checkrows = map_example_filt[map_example_filt[0].str.startswith('>')]

    map_example_filt['concatenated'] = map_example_filt['concatenated'].ffill()
    map_example_filt[['concat_query','concat_target']] = map_example_filt['concatenated'].str.split(' ',expand=True)

    concatenated_q = map_example_filt.pop('concat_query')
    map_example_filt.insert(0,'concat_query',concatenated_q)
    concatenated_t = map_example_filt.pop('concat_target')
    map_example_filt.insert(3,'concat_target',concatenated_t)

    map_example_filt = map_example_filt[~map_example_filt.iloc[:,1].str.startswith('>')]

    map_example_filt = map_example_filt.iloc[:,0:6]

    map_example_filt['concat_query'] = map_example_filt['concat_query'].str.replace('>','')
    map_example_filt = map_example_filt.rename(columns={0:'qstart',1:'qend',2:'tstart',3:'tend'})
    map_example_filt = map_example_filt.astype({'qstart':'int','qend':'int','tstart':'int','tend':'int'})
    
    #check the alignment orientation, either + or -
    map_example_filt['orientation'] = ''

    def orientation_check (df,qstart,qend,tstart,tend,orientation):
        df[orientation] = np.where((df[qend]-df[qstart]>=0) & (df[tend]-df[tstart]>=0),'+','-')
        return(df)

    map_example_filt = orientation_check(map_example_filt, 'qstart', 'qend', 'tstart', 'tend', 'orientation')

    #write out the formatted output into a csv file
    map_example_filt.to_csv(fread + '_prepared.csv',header=False,index=False)
