
# coding: utf-8

# In[33]:
from __future__ import print_function
import pandas as pd
import os
import numpy as np


#csv input
arr = pd.read_csv('gradebook_submit10.csv', quotechar='"', skipinitialspace=True)
snum=int(arr.shape[0])                      #number of students
arr2 = np.empty((2, snum), dtype=object)    #array to key studentIDs to dir names
arr2[0]=arr.as_matrix().T[0]                #StudentIDs from csv

#Directories in the top folder
currDir = '.'
dirs = [ name for name in os.listdir(currDir) if os.path.isdir(os.path.join(currDir, name)) ]

if (len(dirs) < snum):
    print("Warning, ",len(dirs)," directories and", snum," students in the csv!")

#Match studentIDs to directory names
for i in range(0,snum):
    for j in range(0,len(dirs)):
        if(dirs[j].find(arr2[0][i]) > -1):
            arr2[1][i]=dirs[j]
            
print(arr2)


#Change grade:
#arr.set_value(0,arr.keys()[2],5.5)


# In[ ]:



