'''
Created on Aug 23, 2013

this python application makes request to Solor Proxy, extracts a list of volume id
from response, authorizes with OAuth2 server, obtains a token, requests for the volumes 
from Data API, and save the returned stream to a ZIP file.
'''

import configuration
import sys
import urllib
import urllib2
import json
import io
import xml.etree.ElementTree
import os

class SolrRequest:
    def __init__(self):
        self.numfound = 0
        self.volumeLst = []
    
    def getVolumeIds(self, urlprefix, encodedRequest):
        # make Solr request
        url = urlprefix + encodedRequest
        
        # get response
        try:
            # urllib2 module sends HTTP/1.1 requests with Connection:close header included
            print("Sending solr request to " + url)
            response = urllib2.urlopen(url)
            
            # any response other than 200 is viewed as an error
            if (response.code != 200):
                raise urllib2.HTTPError(response.url, response.code, response.read(), response.info(), response.fp)
            
            # a text stream as response
            xmlstream = io.BytesIO(response.read())
            for event, element in xml.etree.ElementTree.iterparse(xmlstream):
                if element.tag == 'result':
                    self.numfound = int(element.attrib['numFound'])
#                     print self.numfound
                if element.tag == 'str' and element.attrib.has_key('name') and \
                    element.attrib['name'] == 'id':
                    self.volumeLst.append(element.text)
#                     print element.text            
            
        # response code in the 400-599 range will raise HTTPError
        except urllib2.HTTPError as e:
            # just re-raise the exception
            raise Exception(str(e.code) + " " + str(e.reason) + " " + str(e.info) + " " + str(e.read()))
        
class DataAPIParameters:
    """ class that wraps Data API requesting url (i.e., /volumes, or /pages, or /tokencount) 
    and parameters    
    """
    
    def __init__(self, url, body):
        self.url = url
        self.body = body
    
    def urlencodedBody(self):
        """ 
        """
        return urllib.urlencode(self.body)

class DataAPIRequest:
    def __init__(self, endpoint, token, parameters):
        self.endpoint = endpoint
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
        urlEncodedBody = self.parameters.urlencodedBody()
        
        # make the request
        # the request method must be POST
        # the body is the urlencoded www form
        # the headers contain OAuth2 token as Authorization, and application/x-www-form-urlencoded as content-type
        req = urllib2.Request(self.endpoint + self.parameters.url, urlEncodedBody, headers)
        try:
            response = urllib2.urlopen(req)
            if (response.code != 200):
                raise urllib2.HTTPError(response.url, response.code, response.read(), response.info(), response.fp)
             
            #  keep the zipcontent in memory
            zipcontent = io.BytesIO(response.read())
             
            return zipcontent
        
        # response code in the 400-599 range will raise HTTPError
        except urllib2.HTTPError as e:
            # just re-raise the exception
            raise Exception(str(e.code) + " " + str(e.reason) + " " + str(e.info) + " " + str(e.read()))


def obtainOAuth2Token(endpoint, clientID, clientSecret):
    """ function that authorizes with OAuth2 token endpoint, obtains and returns an OAuth2 token
    
    arguments:
    clientID -- client ID or username
    clientSecret -- client secret or password
    
    returns OAuth2 token upon successful authroization.
    raises exception if authorization fails
    """
    
    # content-type http header must be "application/x-www-form-urlencoded"
    headers = {'content-type' : 'application/x-www-form-urlencoded'}
     
    # request body
    values = {'grant_type' : 'client_credentials',
          'client_id' : clientID,
          'client_secret' : clientSecret }
    body = urllib.urlencode(values)
     
    # request method must be POST
    req = urllib2.Request(endpoint, body, headers)
    try:
        # urllib2 module sends HTTP/1.1 requests with Connection:close header included
        response = urllib2.urlopen(req)
         
        # any other response code means the OAuth2 authentication failed. raise exception
        if (response.code != 200):
            raise urllib2.HTTPError(response.url, response.code, response.read(), response.info(), response.fp)
         
        # response body is a JSON string
        oauth2JsonStr = response.read()
         
        # parse JSON string using python built-in json lib
        oauth2Json = json.loads(oauth2JsonStr)
         
        # return the access token
        return oauth2Json["access_token"]
    
    # response code in the 400-599 range will raise HTTPError
    except urllib2.HTTPError as e:
        # just re-raise the exception
        raise Exception(str(e.code) + " " + str(e.reason) + " " + str(e.info) + " " + str(e.read())) 

def writeToZipFile(zipcontent, zipfilepath):
    # open file to write
    zf = io.open(zipfilepath, mode='wb')
     
    # read from zip stream
    buf = bytearray(1024)
    size = zipcontent.readinto(buf)
    while (size > 0) :
        zf.write(buf)
        size = zipcontent.readinto(buf)
     
    # close read stream and output file
    print 'Closing zip file'
    zf.close()
    zipcontent.close()

def printUsage():
    print ("UnCampTokenCountDemo.py <zip file>")

def main():        
    if (len(sys.argv) < 2):
        printUsage()
        sys.exit()
    zipfilename = str(sys.argv[1])
    fileExtension = os.path.splitext(zipfilename)[1]
    if (fileExtension != '.zip'):
        print("The output file extension should be zip, e.g., volume.zip. Change it and try again")
        sys.exit()
    
    # call Solr to get a list of volume id
    solrRequest = SolrRequest()
    
    # get volume id from searching metadata
    solrRequest.getVolumeIds(configuration.SOLR_METADATA_URL, urllib.urlencode(configuration.SOLR_METADATA_REQUEST))
    
    # get volume id from searching ocr
#     solrRequest.getVolumeIds(configuration.SOLR_OCR_URL, urllib.quote(configuration.SOLR_OCR_REQUEST))

    # exit if no volume id is returned
    print("Number of volumes read: " + str(len(solrRequest.volumeLst)))
    print("Number of volumes found: " + str(solrRequest.numfound))
    if (len(solrRequest.volumeLst) == 0):
        print("No volume is returned from Solr. Change your request and try again.")
        sys.exit()
        
    # concatenate volume id with pipe '|'
    body = '|'.join(solrRequest.volumeLst)
    
    # get token from OAuth2
    token = obtainOAuth2Token(configuration.OA2_EPR, configuration.OAUTH2_CLIENT_ID, configuration.OAUTH2_CLIENT_SECRET)
    print("Obtained token: " + token)
    
    # fill in data api request parameters
    data = {'volumeIDs' : body}
    data.update(configuration.TOKENCOUNT_PARAMETERS)
    parameters = DataAPIParameters(configuration.TOKENCOUNT_URL_REQUEST, data)
    
    # call Data api
    print("Requesting data from Data API")
    apiRequest = DataAPIRequest(configuration.DATAAPI_EPR, token, parameters)
    zipcontent = apiRequest.request()
    
    # write zip stream to file
    print("Writing to zip file")
    writeToZipFile(zipcontent, zipfilename) 

if __name__ == '__main__':
    main()