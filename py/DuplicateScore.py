# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 10:26:26 2014

@author: mat
"""
import os
import csv
from collections import OrderedDict


def getFiles(folder):
    #get list of files in the folder
    files = os.walk(folder)
    
    dataDict = {}

    #save all the file names
    for root, dirs, file in files:
        fileList = file            
    
    #go through the files and return the data
    for i in range (len(fileList)):

        elem =  folder+'/'+fileList[i]
        #open the file
        with open(elem,'rb') as f:
            reader = csv.reader(f,delimiter='\t',quoting=csv.QUOTE_NONE)
            #read each line of the file
            rows = []
            for row in reader:
                rows.append(row[0])
                
        dataDict[fileList[i]]=[rows]

    return dataDict
    
def compareFields(data):
    
    dup_matrix = []
    fields=[]
    dup_sing_perc = []
    dup_combine_perc = []    
    
    for fieldA in data.keys():
        dup_row = []
        dup_sing = []
        dup_combine = []
        for fieldB in data.keys():
            first = data.get(fieldA)[0]
            second = data.get(fieldB)[0]
            
            #Convert data to sets and find the duplicates (intersections)
            AA = set(map(tuple,first))
            BB = set(map(tuple,second))
            dup_count = len(BB.intersection(AA))
            
            #Append the results to the row
            dup_row.append(dup_count)
            dup_combine.append(float(dup_count)/(float(len(AA)+float(len(BB)))) )
            dup_sing.append(float(dup_count)/float(len(AA)))
        fields.append(fieldA)
    
        #Add the rows to the matrix
        dup_matrix.append(dup_row)
        dup_sing_perc.append(dup_sing)
        dup_combine_perc.append(dup_combine)
        
    return dup_matrix,fields,dup_sing_perc,dup_combine_perc
    
def main():
    print ''
    #Set the folder name
    folder = 'AllYears'
    #Get the files and store in a dict with all publications
    data = getFiles(folder)
    
    data = OrderedDict(sorted(data.items(), key=lambda t:t[0]))

    duplicates,fields,dup_sing_perc,dup_combine_perc = compareFields(data)
    
    with open('Duplicate_results.csv','w') as f:
        #Number of publications that are same
        f.write('\n')
        f.write('Number of publications that are same')
        f.write('\n')
        for i in range(len(fields)):
            if i == 0:
                f.write(',')
            f.write(os.path.splitext(str(fields[i]))[0]+',')
            
        f.write('\n')
        for i in range(len(duplicates)):
            f.write(os.path.splitext(str(fields[i]))[0]+',')
            for j in range(len(duplicates[i])):
                f.write(str(duplicates[i][j])+',')
            f.write('\n')
            
        f.write('\n')
        f.write('Percent of publications that are same per field total arranged by row')
        f.write('\n')
        #Total Percent of publications that are same
        for i in range(len(fields)):
            if i == 0:
                f.write(',')
            f.write(os.path.splitext(str(fields[i]))[0]+',')
            
        f.write('\n')
        for i in range(len(dup_sing_perc)):
            f.write(os.path.splitext(str(fields[i]))[0]+',')
            for j in range(len(dup_sing_perc[i])):
                f.write(str(dup_sing_perc[i][j])+',')
            f.write('\n')
            
        f.write('\n')
        f.write('Percent of publications that are same by total')
        f.write('\n')
            
        #Total Percent of publications that are same
        for i in range(len(fields)):
            if i == 0:
                f.write(',')
            f.write(os.path.splitext(str(fields[i]))[0]+',')
            
        f.write('\n')
        for i in range(len(dup_combine_perc)):
            f.write(os.path.splitext(str(fields[i]))[0]+',')
            for j in range(len(dup_combine_perc[i])):
                f.write(str(dup_combine_perc[i][j])+',')
            f.write('\n')
        
main()