# -*- coding: utf-8 -*-
"""
Created on Fri May 15 17:02:52 2015

This will take the yearly parsed data (from the raw downloaded data) and combine
into a single csv file containing data over all the years.
"""
import os
import sys

def combineFiles(folder,files,combineFolder,field):
     
    #for i in range(len(files)):

    with open(combineFolder+'/'+field+'.txt','w') as outfile:
        for data in files: 
            with open(data) as infile:
                for line in infile:
                    outfile.write(line)
                
def getFiles(folder):
    files = os.walk(folder)
    #save all the file names
    for root, dirs, file in files:
        for i in range(len(file)):
            file[i]=root+'/'+file[i]
        return file

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
            print root
            folders.append(folder)
            field = root.split('/')[1]
            fields.append(field)
    #Return folders and files and splice out top directory
    return folders,fields

def main():
    #Get folder locations
    parsedFolder = 'PARSE_Keyword'
    combineFolder = 'PARSE_ALL'

    folders,fields =getFolders(parsedFolder)
    print folders
    print fields
    #Combine files in field
    #save to folder
    for i in range(len(folders)):
        files = getFiles(folders[i])
        print files
        combineFiles(folders[i],files,combineFolder,fields[i])
    
main()
