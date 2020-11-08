# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 20:46:30 2020

@author: Bahman
"""
import glob
import os
import zipfile
import pandas as pd

col_names =  ['Year',
              'Month',
              'Origin',
              'ArrTime',
              'DepTime',
              'Dest', 
              'ArrDelay', 
              'UniqueCarrier', 
              'DayOfWeek', 
              'DepDelay', 
              'Cancelled']

my_df  = pd.DataFrame(columns = col_names)
my_df.to_csv("CleanedData.csv", encoding='utf-8', index=False)

for dirpath, dirnames, filenames in os.walk("/data/aviation/airline_ontime/"):   
    
    for name in glob.glob(dirpath + '/*.zip'):
        print(name)
        base = os.path.basename(name)
        filename = os.path.splitext(base)[0]
        
        datadirectory = dirpath + '/'
        dataFile = filename
        archive = '.'.join([dataFile, 'zip'])
        fullpath = ''.join([datadirectory, archive])
        csv_file = '.'.join([dataFile, 'csv'])
        
        filehandle = open(fullpath, 'rb')
        zfile = zipfile.ZipFile(filehandle)    
        data = pd.read_csv(zfile.open(csv_file))
        data = data[col_names]
        data.to_csv("CleanedData.csv", encoding='utf-8', index=False, mode='a', header=False)



print(my_df)
    

