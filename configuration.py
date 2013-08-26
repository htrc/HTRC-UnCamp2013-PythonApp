'''
Created on Aug 23, 2013
'''

#######################################################
#       Data API/Solr/OAuth2 parameters setting       #
#######################################################

''' OAuth2 credentials '''
OAUTH2_CLIENT_ID = "PUT_YOUR_CLIENT_ID_HERE"
OAUTH2_CLIENT_SECRET = "PUT_YOUR_CLIENT_SECRET_HERE"

''' Solr request string '''
SOLR_METADATA_REQUEST = {'q' : 'allfields:war AND author:Bill'}
#SOLR_METADATA_REQUEST = {'q':'allfields:war AND author:Bill', 'start':'0', 'rows':'20'}
#SOLR_OCR_REQUEST = 'war'

''' Data API volume request parameters '''
VOLUME_PARAMETERS = {}
# e.g., VOLUME_PARAMETERS = {'mets' : 'false', 'concat' : 'false'}

''' Data API token count request parameters '''
TOKENCOUNT_PARAMETERS = {}
# e.g., TOKENCOUNT_PARAMETERS = {'level' : 'page',    # 'page'
#                         'sortBy' : 'count',  # 'token'
#                         'sortOrder' : 'desc' # 'asc'
#                         } 

##########################################################################
#        Default Data API/Solr/OAuth2 setting (No need to change)        #
##########################################################################
PAGE_URL_REQUEST = "/pages"
VOLUME_URL_REQUEST = "/volumes"
TOKENCOUNT_URL_REQUEST = "/tokencount"

# OA2_EPR = "https://htrc3.pti.indiana.edu:9443/oauth2endpoints/token?grant_type=client_credentials"
# DATAAPI_EPR = "https://htrc4.pti.indiana.edu:25443/data-api"

OA2_EPR = "https://sandbox.htrc.illinois.edu:9443/oauth2endpoints/token?grant_type=client_credentials"
DATAAPI_EPR = "https://sandbox.htrc.illinois.edu:25443/data-api"
SOLR_METADATA_URL = "http://chinkapin.pti.indiana.edu:9446/solr/meta/select?"
SOLR_OCR_URL = "http://chinkapin.pti.indiana.edu:9446/solr/ocr/select?q=ocr:"

