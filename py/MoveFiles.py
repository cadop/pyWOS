# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 09:12:21 2015

@author: cadop

Move files from individual folders with yearly files to year based folders
"""

import os
import shutil
import errno

def getFiles(folder):
    files = os.walk(folder)
    #save all the file names
    for root, dirs, file in files:
        if len(file)!=0:
            for i in range(len(file)):
                file[i]=root+'/'+file[i]
        
            return file
        else:
            return None

def getFolders(folder):
    #get list of files in the folder
    files = os.walk(folder)
    folders = []
    fields = []
    #save all the file names
    for root, dirs, file in files:
        sub_folder = os.path.basename(root)
        folder = root

        if sub_folder != root:
            folders.append(folder)
            field = root.split('/')[1]
            fields.append(field)
    #Return folders and files and splice out top directory
    return folders,fields
    
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
            
def main():
    folder = 'Yearly/'
    folders,fields = getFolders(folder)
    files = []
    for item in folders:
        data = getFiles(item)
        if data!=None:
            files.append(data)
        
    saveFolder = 'YearsSeperate'
    
    years = ['2009','2010','2011','2012','2013','2014']
    organizedFiles = [[],[],[],[],[],[]]
    for file in files:
        for item in file:
            for i in range(len(years)):
                if item.split('_')[1].rstrip('.txt') == years[i]:

                    organizedFiles[i].append(item)
                    
    for year in organizedFiles:
        for file in year:
            srcfile = file
            dstdir = saveFolder+'/'+file.split('_')[1].rstrip('.txt')+'/'
            make_sure_path_exists(dstdir)
            shutil.copy(srcfile, dstdir)

main()