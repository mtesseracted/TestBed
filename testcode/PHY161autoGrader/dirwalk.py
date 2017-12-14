#!/usr/bin/python
#Easiest method to enter grades:
#  find studentID as the string inside () in dir name
#  import csv file with corrent headers and studentIDs into array
#  use studentID as key to replace appropriate grade value in array
#  save modded array as csv, then upload

#CSV upload:
#To get the format that sakai wants you can first go to:
#Gradebook -> Import/Export, then click "Export Gradebook", it should default be csv

#The resulting CSV will obtain all studentIDs, gradebooks items and their corresponding grades,
#  For ease I would recommend doing this @beginning of semester b/c you need to delete all
#  gradebook items but 1, and the corresponding fields.  If not @beginning prob easier to import
#  into excel and manipulate there.  Then rename the grade assignment and value in square brackets
#  as grade point max as desired.  Also modify the * AssignmentName field as the corresponding
#  comments for a submission.

#To upload: (The assignment can exist already or not, just not be locked)
#Gradebook -> Import/Export, then click "Choose File", select appropriate file, then upload.
#  Now you should check the box for the assignment and click next, if it exists already it will default
#  import with that assignment, if not it was go through the assignment creation.  If and invalid StudentID
#  is found it will also alert you. 

#Have seperate log file that reports missing/extra students and errors when grading 

import os

# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk("."):
    path = root.split(os.sep)
    print((len(path) - 1) * '---', os.path.basename(root))
    for file in files:
        print(len(path) * '---', file)
