# -*- coding: utf-8 -*-
"""
Parse the RAW XML data from the WOS API downloader.
Save to a csv file
"""

#Should parse data as
# UID, Authors, Article Name, Journal Name, Year
#Using TAB to deliminate

import xml.etree.ElementTree as ET
import csv
import os
import sys

def parseRow(root):
    #initiate some variables for the return incase they are not found
    # they will just be blank
    author_keywords = ''
    keywords_plus = ''
    
    # .text = value inbetween tags
    # .child = child of tag
    # .attrib = values inside of tag
    for child in root:
        #Get Unique ID
        if child.tag == 'UID':
            uid = str(child.text)
        elif child.tag =='static_data':
            for subchild in child:
                if subchild.tag == 'summary':
                    #Get Year and Type
                    for summaries in subchild:
                        if summaries.tag == 'pub_info':
                            pub_year =  summaries.attrib.get('pubyear').encode('utf-8')
                            pub_type = summaries.attrib.get('pubtype').encode('utf-8')
                        #Get journal and article name
                        elif summaries.tag == 'titles':
                            for title in summaries:
                                if title.attrib.get('type') == 'source':
                                    journal_name = title.text.encode('utf-8')                              
                                elif title.attrib.get('type') == 'item':
                                    article_name = title.text.encode('utf-8')
                        #Get authors
                        elif summaries.tag == 'names':
                            authors = ''
                            for a in range(len(summaries)):
                                for names in summaries[a]:
                                    if names.tag == 'full_name':
                                        if authors == '':
                                            authors = names.text.encode('utf-8')
                                        else:
                                            authors = authors + ';'+names.text.encode('utf-8')
                elif subchild.tag == 'fullrecord_metadata':
                    for metadata in subchild:
                        if metadata.tag == 'addresses':
                            addresses = ''
                            # The addresses, like many of the xml file, is nested with many options
                            # the one we want is full address, so we will make a loop to go through all the items
                            # for each sub section, until we reach the sub section that contains full address
                            # once we reach that, we will go through those items, but use the if statement
                            # to find when the tag is the one we want, then get that information
                            for a in range(len(metadata)):
                                for b in range(len(metadata[a])):
                                    for address in metadata[a][b]:
                                        if address.tag == 'full_address':
                                            if addresses == '':
                                                #It seems some address has semicolon, so remove it because we use it to separate addresses
                                                addresses = address.text.encode('utf-8').replace(';',' ')
                                            else:
                                                addresses = addresses + ';'+address.text.encode('utf-8').replace(';',' ')
                        elif metadata.tag == 'keywords':
                            author_keywords = ''
                            for keyword in metadata:
                                if keyword.tag=='keyword':
                                    if author_keywords == '':
                                        author_keywords = keyword.text.encode('utf-8')
                                    else:
                                        author_keywords = author_keywords + ';' + keyword.text.encode('utf-8')
                        
                elif subchild.tag == 'item':
                    for items in subchild:
                        if items.tag == 'keywords_plus':
                            for keyword in items:
                                if keyword.tag == 'keyword':
                                    if keywords_plus == '':
                                        keywords_plus = keyword.text.encode('utf-8')
                                    else:
                                        keywords_plus = keywords_plus + ';' + keyword.text.encode('utf-8')
        
    return [uid,authors,article_name,journal_name,pub_year,pub_type, addresses,author_keywords,keywords_plus]                          

def getFiles(folder):
    #get list of files in the folder
    files = os.walk(folder)
    fileList = []
    folders = []
    #save all the file names
    for root, dirs, file in files:
        fileList.append(file)
        path = root.split('/')
        folder = os.path.basename(root)
        folder = root
        folders.append(folder)
    #Return folders and files and splice out top directory
    return [folders[1:],fileList[1:],path]
    
def main():    
    #Name of folder containing the RAW Data
    raw_folder = 'RAW_Keyword'    
    folderList,fileList,path = getFiles(raw_folder) 
    #Folder to save the Parsed Datat to
    parse_folder = 'PARSE_Keyword'
    
    for folder in range(len(folderList)):
        for files in range(len(fileList[folder])):
            cur_file = fileList[folder][files]
            cur_folder = folderList[folder]
            subfolder = cur_folder.lstrip(raw_folder)
            
            readfile = cur_folder+'/'+cur_file
            writefile = parse_folder+subfolder+'/'+cur_file.strip('.xml')+'.txt'
            if not os.path.exists(parse_folder+subfolder):
                os.makedirs(parse_folder+subfolder)
            print 'Reading: ',readfile
            sys.stdout.flush()
            print 'Writing: ',writefile
            print ''
            sys.stdout.flush()
            
            #Open the file to read from (raw data)
            infile = open(readfile)

            data = []
            for line in infile:
                if line.startswith('<REC '):
                    data.append(line)
                   
            #Close the raw data file
            infile.close()
            
            #Open the file to write to (parsed data)            
            with open(writefile,'wb') as outfile:
                writer = csv.writer(outfile,delimiter='\t') 
                for i in range(len(data)):
                    row = parseRow(ET.fromstring(data[i]))
                    writer.writerow(row)
                    
            print 'Finished'
            sys.stdout.flush()
            #outfile.close()
    
main()