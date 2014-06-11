#-------------------------------------------------------------------------------
# Name:        smallfolderarranger
# Purpose:
#
# Author:      Joakim
#
# Created:     10.06.2014
# Copyright:   (c) Joakim 2014
#-------------------------------------------------------------------------------

#Script to delete folders with x<=4 pictures after moving them to a separate folder.

import os
import shutil

#path for which to look through image-folders
path=os.getcwd() + u'/test'
folderpath=path + u'/pictures'
print folderpath
print path

if not os.path.isdir(folderpath):
    print 'mkdir'
    os.mkdir(folderpath)


for folder in os.listdir(path):
    #hvis mappen har mindre eller lik 4 bilder
    currentpath=path+u'/'+folder
    print currentpath

    print not (currentpath == folderpath)
    if len(os.listdir(currentpath))<=4 and not (currentpath == folderpath):
        print 'deleting'
        #så kopierer vi bildene, og sletter mappa
        for FILE in os.listdir(currentpath):
            filepath=currentpath+'/'+FILE
            topath=folderpath+u'/'+FILE
            shutil.copy2(filepath, topath)
        shutil.rmtree(currentpath)
