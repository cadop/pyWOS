# -*- coding: utf-8 -*-
"""
Created on Thu Apr 02 17:58:45 2015

@author: cadop
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from suds.client import Client
from suds.transport.http import HttpTransport
import urllib2
import sys
import time
import os
import errno



class HTTPSudsPreprocessor(urllib2.BaseHandler):
    def __init__(self, SID):
        self.SID = SID

    def http_request(self, req):
        req.add_header('cookie', 'SID="'+self.SID+'"')
        return req

    https_request = http_request

class WokmwsSoapClient():
    """
    main steps you have to do:
        soap = WokmwsSoapClient()
        results = soap.search(...)
    """
    def __init__(self):
        self.url = self.client = {}
        self.SID = ''

        self.url['auth'] = 'http://search.webofknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl'
        self.url['search'] = 'http://search.webofknowledge.com/esti/wokmws/ws/WokSearch?wsdl'

        self.prepare()

    def __del__(self):
        self.close()

    def prepare(self):
        """does all the initialization we need for a request"""
        print ''
        print '***Preparing Connection***'        
        self.initAuthClient()
        self.authenticate()
        self.initSearchClient()
        print '***Finished Preparing Connection***'
        print ''

    def initAuthClient(self):
        print 'initialize authentication...'
        self.client['auth'] = Client(self.url['auth'])

    def initSearchClient(self):
        print 'initialize search....'
        http = HttpTransport()
        opener = urllib2.build_opener(HTTPSudsPreprocessor(self.SID))
        http.urlopener = opener
        self.client['search'] = Client(self.url['search'], transport = http)
        print 'searching initializtion done'

    def authenticate(self):
        self.SID = self.client['auth'].service.authenticate()
        print 'authenticating initialization done'

    def close(self):
        self.client['auth'].service.closeSession()

    def search(self, query,filename):
        MAX_RECORDS = 100
        #query parameters
        qparams = {
            'databaseId' : 'WOS',
            'userQuery' : query,
            'queryLanguage' : 'en',
            'editions' : [{
                'collection' : 'WOS',
                'edition' : 'SCI',
            },{
                'collection' : 'WOS',
                'edition' : 'SSCI',
            }]
        }
        #retrive parameters
        rparams = {
            'count' : MAX_RECORDS, # 1-100
            'firstRecord' : 1,
            'sortField' : [{
                #'name' : 'RS', #Relevance
                'name' : 'LD',
                'sort' : 'D', #Descending
            }]#,
            #'viewField' : [{
                #'collectionName' : 'WOS',
#                'fieldName' : 'names',
#                'fieldName' : 'titles',
#                'fieldName' : 'addresses',
                #'fieldName' : 'names'
#                'fieldName' : 'keywords_plus'
            #}]
        }
        result = self.client['search'].service.search(qparams, rparams)
        queryId = int(result.queryId)
        recordsFound = int(result.recordsFound)
        outFile = open(filename+'.xml', 'w')
        print "Starting: ",filename
        print 'Total Records Found: ',recordsFound
        cur_record = 1
        while rparams['firstRecord'] < recordsFound:
            try:
                cur_record = rparams.get('firstRecord')
                #if rparams['firstRecord'] != 1: # FUTURE OPTIMIZATION?
                remainingRecords = recordsFound - rparams['firstRecord']
                rparams['count'] = MAX_RECORDS
                if remainingRecords < MAX_RECORDS:
                    rparams['count'] = remainingRecords
                print "Retrieving " + str(rparams['firstRecord']) + "->" + str(rparams['count']+rparams['firstRecord']-1)
                result = self.client['search'].service.retrieve(queryId, rparams)
                rparams['firstRecord'] += MAX_RECORDS
                if rparams.get('firstRecord') > 99900 and rparams.get('sortField')[0].get('sort')=='D':
                    rparams['sortField'][0]['sort']='A'
                    rparams['firstRecord'] = 1
                elif rparams.get('firstRecord') >99900 and rparams.get('sortField')[0].get('sort') == 'A':
                    break
                outFile.write(result.records.encode('utf-8'))
            except Exception,e:
                print 'error'
                print e
                time.sleep(5)
                try:
                    cur_record = rparams.get('firstRecord')
                    #if rparams['firstRecord'] != 1: # FUTURE OPTIMIZATION?
                    remainingRecords = recordsFound - rparams['firstRecord']
                    rparams['count'] = MAX_RECORDS
                    if remainingRecords < MAX_RECORDS:
                        rparams['count'] = remainingRecords
                    print "Retrieving " + str(rparams['firstRecord']) + "->" + str(rparams['count']+rparams['firstRecord']-1)
                    result = self.client['search'].service.retrieve(queryId, rparams)
                    rparams['firstRecord'] += MAX_RECORDS
                    if rparams.get('firstRecord') > 99900 and rparams.get('sortField')[0].get('sort')=='D':
                        rparams['sortField'][0]['sort']='A'
                        rparams['firstRecord'] = 1
                    elif rparams.get('firstRecord') >99900 and rparams.get('sortField')[0].get('sort') == 'A':
                        break
                    outFile.write(result.records.encode('utf-8'))
                    
                except Exception,e:
                    print 'still in error'
                    print e
                    time.sleep(61)
                    try:
                        result = self.client['search'].service.search(qparams, rparams)
                        queryId = int(result.queryId)
                        recordsFound = int(result.recordsFound)

                    except Exception,e:
                        print 'who knows, its just broken'
                        print e
                        break
                
        print "Finished: ",filename
#        return self.client['search'].service.search(qparams)

#import getKeywords   
def main():
    #Try to request only specific items
    db_connection = WokmwsSoapClient()

    #Query delay = 2 times per second
    #Authentication 1 time per minute
    #Count max 100
    #Query return up to 100,000
    
    #Save only needed info: UniqueID,Title,Journal,Year,Article,
    # Authors,Address,Keywords,KeywordsPlus
    

    #Example list of keywords
    keywords = ['Math','Science']
    #Years to download for each keyword
    years = ['2009','2010','2011','2012','2013','2014']

    count = 1
    firstRecord = 1
    folder = 'Data/'
    for i in range(len(keywords)):
        firstRecord = 1
        for j in range(len(years)):
            #Get total publications
            #Set maximum of firstRecord to total publications
            #Save required data in folder/file:  Field/Year/Range.csv
            tmpfolder = folder+str(keywords[i])+'/'
            filename = tmpfolder+str(keywords[i])+'_'+str(years[j])
            make_sure_path_exists(tmpfolder)
            print 'Sending: ',keywords[i]
            
            #Use AD for address, TS for topic, PY for year.  
            db_connection.search('AD=%s AND PY=%s'%(keywords[i],years[j]),filename)
    
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
            
main()
