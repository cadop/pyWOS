# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 16:21:38 2015

Retrieves the most frequent journals, sorts by frequency while preserving
the article ID corresponding to each journal occurance.

Can be used to measure duplicates within a certain rank.

@author: cadop
"""

import os
import csv
import sys
from collections import OrderedDict
from collections import Counter

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def getFiles(folder,year):
    #get list of files in the folder
    if year!=None:
        folder = folder+'/'+year+'/'    
    print folder
    files = os.walk(folder)
    
    dataDict = {}
    
    #save all the file names
    for root, dirs, file in files:
        fileList = file            

    #go through the files and return the data
    if year!=None:
        for i in range (len(fileList)):
    
            elem =  folder+'/'+fileList[i]
            #open the file
            with open(elem,'rb') as f:
                reader = csv.reader(f,delimiter='\t',quoting=csv.QUOTE_NONE)
                #read each line of the file
                rows = []
                for row in reader:
                    if row[4] == year:
                        rows.append((row[0],row[3]))
                    
            dataDict[year+'_'+fileList[i]]=[rows]
    
        return dataDict
    
    else:
        for i in range (len(fileList)):
            elem =  folder+'/'+fileList[i]
            #open the file
            with open(elem,'rb') as f:
                reader = csv.reader(f,delimiter='\t',quoting=csv.QUOTE_NONE)
                #read each line of the file
                rows = []
                for row in reader:
                    rows.append((row[0],row[3]))
                    
            dataDict[fileList[i]]=[rows]
    
        return dataDict
    
def journalCount(data):
    journal_names = []
#    print len(data)
    for i in range(len(data)):
        journal_names.append(data[i][1])
        
    counts = Counter(journal_names)

    journal_group = {}
    for item in data:
        journal_group.setdefault(item[1], []).append(item)

    journal_res = []
    group_counts = Counter({f: len(items) for f,items in journal_group.iteritems()})
    #Iterate throught the most common journals (change number to include more journals)
    for journal, count in group_counts.most_common(100000):
        journal_res.append(journal_group[journal])
                    
    sys.stdout.flush()
    return journal_res

            
def writeTotals(journals,folders):
    
    #Declare an ordered dict that will hold the field, then the journal totals in that field 
    total_list = OrderedDict()
    
    for field in journals:
       # print 'Field: ',field[1]
        totals = []
        for i in range(len(field[0])):
            #print 'Journal: ',field[0][i][0][1],' Length',len(field[0][i])
            totals.append([field[0][i][0][1],len(field[0][i])])
        total_list[field[1]] = totals
        
    for key in total_list:   
        writeto = folders[0]+key.split('_')[0]+'/'
        writeto = folders[0]
        make_sure_path_exists(writeto)
        print 'Key: ',key
        #with open(writeto+key.split('_')[1]+'.csv','w') as outfile:
        with open(writeto+key.split('.')[0]+'.csv','w') as outfile:
            for i in range(len(total_list.get(key))):
                outfile.write(str('"'+total_list.get(key)[i][0])+'",'+str(total_list.get(key)[i][1])+'\n')
        
    for key in total_list:   
        writeto = folders[1]+key.split('_')[0]+'/'
        writeto = folders[1]
        make_sure_path_exists(writeto)
        #with open(writeto+key.split('_')[1]+'.csv','w') as outfile:
        with open(writeto+key.split('.')[0]+'.csv','w') as outfile:
            for i in range(len(total_list.get(key))):
                outfile.write(str(i+1)+','+str(total_list.get(key)[i][1])+'\n')
            
def main():
    print ''
    #Set the folder name
    folder = 'AllYears'
    #folder = 'YearsSeperate'
    #Get the files and store in a dict with all publications
    foldersOut = ['JournalLists/','JournalNumbers/']

    #years = ['2009','2010','2011','2012','2013','2014']
    years = None
    
    data = []
    if years!=None:
        for year in years:
            data.append(getFiles(folder,year))
    else:
        data.append(getFiles(folder,None))
    
    for datum in data:
        journals = []
        for key in datum:
            journals.append([journalCount(datum.get(key)[0]),key])

        writeTotals(journals,foldersOut)   

    
main()