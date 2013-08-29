'''
Created on Aug 23, 2013

this python application makes request to Solor Proxy, extracts a list of volume id
from response, authorizes with OAuth2 server, obtains an OAuth2 token, requests for 
volume content from Data API, and saves the volume content to a ZIP file.
'''

import uncamputils
import sys
import urllib
import urllib2
import io
import xml.etree.ElementTree
import os

''' OAuth2 credentials '''
OAUTH2_CLIENT_ID = "PUT_YOUR_CLIENT_ID_HERE"
OAUTH2_CLIENT_SECRET = "PUT_YOUR_CLIENT_SECRET_HERE"

''' Data API volume request parameters '''
PAGE_PARAMETERS = {}
# PAGE_PARAMETERS = {'mets':'true'}
# PAGE_PARAMETERS = {'mets':'false', 'concat':'true'}
# NOTE: "concat" and "mets" cannot be both set

''' Solr request string '''
SOLR_METADATA_REQUEST = {'q' : 'title:war AND author:Bill'}
# SOLR_METADATA_REQUEST = {'q' : 'publishDate:1884 AND author:Dickens'}
# SOLR_METADATA_REQUEST = {'q' : 'publishDate:1884 AND author:Dickens', 'fl' : 'id'}

class SolrRequest:
    ''' This class sends requests to Solr Proxy and parse the response to get a list of volume id.     
    '''
    
    def __init__(self):
        self.numfound = 0
        self.volumeList = []
    
    def getVolumeIds(self, serverurl, encodedRequest):
        # make Solr request
        solrQueryReq = serverurl + encodedRequest
        
        # get response
        # urllib2 module sends HTTP/1.1 requests with Connection:close header included
        print("Sending solr request to " + solrQueryReq)
        response = urllib2.urlopen(solrQueryReq)
        
        # any response other than 200 is viewed as an error
        if (response.code != 200):
            raise urllib2.HTTPError(response.url, response.code, response.read(), response.info(), response.fp)
        
        # parse solr response into a list of volume id 
        solrresponse = io.BytesIO(response.read())
        for event, element in xml.etree.ElementTree.iterparse(solrresponse):
            if element.tag == 'result':
                self.numfound = int(element.attrib['numFound'])
            if element.tag == 'str' and element.attrib.has_key('name') and \
                element.attrib['name'] == 'id':
                self.volumeList.append(element.text)    

class DataAPIRequest:
    ''' This class sends requests to Data API to retrieve data.     
    '''
    
    def __init__(self, endpoint, requesturl, token, parameters):
        self.endpoint = endpoint
        self.requesturl = requesturl
        self.token = token
        self.parameters = parameters
        
    def request(self):
        """ function that sends request to Data API service and returns a zip stream 
        
        returns zip stream upon successful authroization.
        raises exception if any HTTP error occurs
        """
        
        # 2 http request headers must be present
        # the Authorization header must be the OAuth2 token prefixed with "Bearer " (note the last space)
        # and the Content-type header must be "application/x-www-form-urlencoded" 
        headers = {"Authorization" : "Bearer " + self.token,
               "Content-type" : "application/x-www-form-urlencoded"}
        
        # urlencode the body query string
        urlEncodedBody = urllib.urlencode(self.parameters)
        print("urlEncodedBody " + urlEncodedBody)
        
        # make the request
        # the request method must be POST
        # the body is the urlencoded www form
        # the headers contain OAuth2 token as Authorization, and application/x-www-form-urlencoded as content-type
        req = urllib2.Request(self.endpoint + self.requesturl, urlEncodedBody, headers)
        print("Sending data api request to " + self.endpoint + self.requesturl)
        response = urllib2.urlopen(req)
        if (response.code != 200):
            raise urllib2.HTTPError(response.url, response.code, response.read(), response.info(), response.fp)
         
        #  keep the zipcontent in memory
        zipcontent = io.BytesIO(response.read())
        return zipcontent

def main():        
    if (len(sys.argv) < 2):
        print ("UnCampVolumeDemo.py <zip file>")
        sys.exit()
    zipfilename = str(sys.argv[1])
    fileExtension = os.path.splitext(zipfilename)[1]
    if (fileExtension != '.zip'):
        print("The output file extension should be zip, e.g., volume.zip. Change it and try again")
        sys.exit()
    
    # call Solr to get a list of volume id
    solrRequest = SolrRequest()
    
    # get volume id from searching metadata
    solrRequest.getVolumeIds(uncamputils.SOLR_METADATA_URL, urllib.urlencode(SOLR_METADATA_REQUEST))
    
    # get volume id from searching ocr
#     solrRequest.getVolumeIds(uncamputils.SOLR_OCR_URL, urllib.quote(SOLR_OCR_REQUEST))

    # exit if no volume id is returned
    print("Number of volumes read: " + str(len(solrRequest.volumeList)))
    print("Number of volumes found: " + str(solrRequest.numfound))
    if (len(solrRequest.volumeList) == 0):
        print("No volume is returned from Solr. Change your request and try again.")
        sys.exit()
    
    # append page number to each volume id
    idList = [id + '[1,5,10]' for id in solrRequest.volumeList] 
    
    # concatenate volume id with pipe '|'
    pageIdList = '|'.join(idList)
    
    # get token from OAuth2
    token = uncamputils.obtainOAuth2Token(uncamputils.OA2_EPR, OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET)
    print("Obtained token: " + token)
    
    # fill in data api request parameters
    parameters = {'pageIDs' : pageIdList}
    parameters.update(PAGE_PARAMETERS)
    
    # call Data api
    print("Requesting data from Data API")
    apiRequest = DataAPIRequest(uncamputils.DATAAPI_EPR, uncamputils.PAGE_URL_REQUEST, token, parameters)
    zipcontent = apiRequest.request()
    
    # write zip stream to file
    print("Writing to zip file")
    uncamputils.writeZipFile(zipcontent, zipfilename) 

if __name__ == '__main__':
    main()