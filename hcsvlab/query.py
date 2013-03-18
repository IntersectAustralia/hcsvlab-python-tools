'''
Created on 11/03/2013

@author: ilya
'''
#import json
import requests
import os.path
import sys
import argparse

class Query(object):
    '''
    classdocs
    '''
    

    def __init__(self, url="http://gsw1-hcsvlab-test3-vm.intersect.org.au:8080/documents.json"):
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
                sys.stdout.write("\rDownloading file {0} of {1}: {2}".format(file_count, total, filename))
                outfile.write(requests.get(url).text.encode('utf8'))
                outfile.close()
                file_count += 1
            sys.stdout.write('\n')
            print "Success! %s files downloaded to '%s'" % (total, directory)
        except:
            print "No query has been executed"

    @staticmethod
    def parse_params(params_str):
        try:
            params_list = params_str.split(",")
            params_hash = {}
            for param in params_list:
                p = param.split("=")
                params_hash[p[0]] = p[1]
            return params_hash
        except:
            print "Couldn't parse params"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download corpus documents based on query")

    parser.add_argument("url", metavar="url",
                      help="documents list url")

    parser.add_argument("corpus_dir", metavar="corpus_dir",
                      help="directory to download corpus to")

    parser.add_argument("query",
                      help="documents query string", nargs='?')

    namespace, extra = parser.parse_known_args()

    try:
        if namespace.query:
            params = Query.parse_params(namespace.query)
        else:
            params = {}
        
        query = Query(namespace.url)
        query.query(params)
        #query.summary()
        query.download(namespace.corpus_dir)
    except:
        print "Could not download documents"
            

