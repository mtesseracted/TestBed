
# coding: utf-8

# In[111]:

#########################################################
#Program: Grader for PHY161L
#Author: Aaron Mahler
#
#Dependencies: All standard python libraries
#
#Inputs: Requires the sakai directory structure for
#   downloaded submission of Student/Submission
#   Directory/files.  Change the hardcoded file
#   names below to match submission folder name,
#   csv file of grades(graCSV), and grader file 
#   name(cfil).
#
#Outputs: Prints messages to stdout, recommend redirect
#   to desired log file.  Will save grades in csv file
#   with  name graCSV+graded.  The grading script 
#   output is redirected to 2>errlog
#
#Version:   Date:      Comments:
#0.0        24FEB17    
#########################################################

from __future__ import print_function #force python3 print()
import pandas as pd
import os
import numpy as np
import subprocess as sp

#Hard-Code File names, extensions, etc
graCSV = "gradebook_submit10.csv" #Empty (of grades) csv file with studentIDs
subF = str("Submission attachment(s)") #submission folder name from sakai
cfil = "alm_hw1check" #Name of check file, to concatenate with submitted file
ext1 = ".ipynb" #extension of submissions
ext2 = ".py" #python extension
dummyFile = "dum1.csv" #dummy file to pass info from grading scipt back to this program

#gradebook csv input
arr = pd.read_csv(graCSV, quotechar='"', skipinitialspace=True)
gkey = arr.keys()[2] #Grade key
ckey = arr.keys()[3] #Comment Key
snum=int(arr.shape[0])                      #number of students
arr2 = np.empty((2, snum), dtype=object)    #array to key studentIDs to dir names
arr2[0]=arr.as_matrix().T[0]                #StudentIDs from csv


#Directories in the top folder
currDir = '.'
dirs = [ name for name in os.listdir(currDir) if os.path.isdir(os.path.join(currDir, name)) ]

if (len(dirs) != snum):
    print("Warning, ",len(dirs)," directories and", snum," students in the csv!")

#Match studentIDs to directory names
for i in range(0,snum):
    for j in range(0,len(dirs)):
        if(dirs[j].find(arr2[0][i]) > -1):
            arr2[1][i]=dirs[j]


# In[106]:

#Set Grade & Comment
#   grade1: float of grade
#   comment1: comment of score
#   array: DataFrame of grades
#   index: student index in array (row #)
#   gkey: key in array for grade column
#   ckey: key in array for comment column
def setGrade(grade1, comment1, array, index, gkey, ckey):
    array.set_value(index,gkey,grade1)
    array.set_value(index,ckey,comment1)    


#bash execute command
def bexec(cmd1):
     return( sp.call(["bash","-c",cmd1]) )

#Find and Replace a string throughout a file with perl thru bash
def bashRep(strFind,strRep,file1):
    cmd1 = str("perl -p -i -e 's/")
    cmd1 += strFind
    cmd1 += str("/")
    cmd1 += strRep
    cmd1 += str("/g' ")
    cmd1 += file1
    return(bexec(cmd1)) #return if errors

#grade a submitted file with a grading file that will be concatenated
#   with the submitted file and store result in dummyFile
def grade(subFile,gradFile):
    dfil=dummyFile #dummy file to pass grade and comment back to this program

    #surround files with quotes to avoid whitespace errors
    sf1 = "\"" + subFile + ext1 + "\"" #submission file with .ipynb
    sf2 = "\"" + subFile + ext2 + "\"" #submission file with .py
    gf2 = "\"" + gradFile + ext2 + "\"" #grading file with .py
    catFile = "\""+subFile+"+grader"+ext2+"\""#sub file cat'd with grad file

    bexec("jupyter nbconvert --to python "+sf1) #Convert from .ipynb to .py 
    bexec("cat " + sf2 + " " + gf2 + " >" + catFile) #concatenate grader file
    str1 = "get_ipython"
    bashRep( str1,"#"+str1, catFile) #remove matplotlib inline
    str1 = "pl.show"
    bashRep(str1,"#"+str1, catFile) #Dont show plots
    bexec("mv " + catFile + " " +currDir) #mv cat file to currDir
    #if running in top directory dont need to move datafile, just have in this location
    print( "Running Grader: " )
    #need to strip directory from name now
    cf2_path, cf2 = os.path.split(catFile[1:-1])
    print( bexec("python \""+cf2+"\" "+dfil+" 2>>errlog") )
   
    dArr = pd.read_csv(dfil, skipinitialspace=True)
    ckey = dArr.keys()[1] #Comments Key
    gkey = dArr.keys()[2] #Grade Key
    gread = str(dArr.get_value(0,gkey))
    cread = str(dArr.get_value(0,ckey))
    return (gread, cread)


# In[109]:

for i in range(snum): #Go over all students in gradebook
    
    print("\n==== Checking StudentID: "+arr2[0][i]+" ====")
    if( str(arr2[1][i]) != "None" ): #Check for folder corresponding to studentID
        
        #check the submission folder
        for root, dirs, files in         os.walk(os.path.join(currDir,arr2[1][i],subF), topdown=True):
            found = 0
            for name in [f for f in files if not f[0] == '.']: #ignore hidden directories
                fnam, fext = os.path.splitext(name)
                if( fext == ext1 ) :
                    found += 1
                    print("--ipynb found--: " + fnam)
                    if (found == 1) :                 
                        g1, c1 = grade(os.path.join(root, fnam), cfil)
                        print("Grade, Comment: ")
                        print(g1)
                        print(c1)
                        print("---------------")
                    else :                       
                        print("!!!DUPLICATES!!!, found "+str(found-1))
                        g2, c2 = grade(os.path.join(root, fnam), cfil)
                        print("Grade, Comment: ")
                        print(g2)
                        print(c2)
                        print("---------------")
                        if(g2>g1): #replace g1 & c1 with max
                            g1 = g2
                            c1 = c2

            #print('---')
            if found == 0 :
                com1 = "No ipynb found. "                
                print(com1)
                setGrade(0.0, com1, arr, i, gkey, ckey)
            elif found == 1:
                setGrade(g1, c1, arr, i, gkey, ckey)
            else :
                com1 = str(found)+" different ipynb's found. Max Grade Comment: "
                setGrade(g1, com1+c1, arr, i, gkey, ckey)
    
    else : #No folder found with that studentID
        com1 = "No submission. "
        print(com1)
        setGrade(0.0, com1, arr, i, gkey, ckey)


# In[110]:




# In[ ]:

gnam, gext = os.path.splitext(graCSV)
gnam += "+graded"
gnam += gext
arr.to_csv(gnam)


# In[ ]:




# In[ ]:



