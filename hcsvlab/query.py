'''
Created on 11/03/2013

@author: ilya
'''
#import json
import requests
import os.path
import sys

class Query(object):
    '''
    classdocs
    '''
    

    def __init__(self, url="http://gsw1-hcsvlab-test3-vm.intersect.org.au/documents.json"):
        '''
        Constructor
        '''
        self.url = url
    
    
    def query(self, query_dict):
        self.query_dict = query_dict
        self.resp_dict = requests.get(self.url, data=query_dict).json()

            
    def summary(self):
        try:
            print "Corpora: %s" % self.query_dict.get('corpus_name', 'all')
            print "Types: %s" % self.query_dict.get('media_type', 'all')
            print "Year range: %s - %s" % (self.query_dict.get('year_from', 'any year'), self.query_dict.get('year_to', 'any year')) 
            print "Number of files: %s" % len(self.resp_dict)
        except:
            print "No query has been executed"

        
    def download(self, directory):
        try:
            if not os.path.isdir(directory):
                os.makedirs(directory)
            urls = [document['url'] for document in self.resp_dict]
            file_count = 1
            total = len(urls)
            for url in urls:
                filename = url.split('/')[-1]
                outfile = open(os.path.join(directory, filename), 'w')
                sys.stdout.write("\rDownloading file {0} of {1}".format(file_count, total))
                outfile.write(requests.get(url).text)
                outfile.close()
                file_count += 1
            sys.stdout.write('\n')
            print "Success! %s files downloaded to '%s'" % (total, directory)
        except:
            print "No query has been executed"
            

