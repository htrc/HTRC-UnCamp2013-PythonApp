Steps below show you how to run the demo applications against our Data API and Solr Proxy. The applications have been tested on Python 2.7.5.

1.	Get your client id and client secret from [URL]. Data API is protected by Oauth2 authetication. You need client id and client secret to access the Data API.

2.	Download the demo archive from [URL].

3.	Unzip the archive. You will see files "configuration.py", "UnCampVolumeDemo.py", and "UnCampTokenCountDemo.py" under folder "uncampclient2013"

4.	Edit your client id and client secret in OAUTH2_CLIENT_ID and OAUTH2_CLIENT_SECRET defined in configuration.py. A sample setting is as follows.
OAUTH2_CLIENT_ID = "YOUR_CLIENT_ID"
OAUTH2_CLIENT_SECRET = "YOUR_CLIENT_SECRET"

5.	Run the demos by typing following command. Assume your command line terminal is under folder "uncampclient2013".
> python UnCampVolumeDemo.py volume.zip
This demo sends Solr query string ["XXX"] to Solr proxy, extracts volume id from XML returned, sends the volume id list to Data API to download contents of the volumes and finally saves the contents in a zip file whose name is provided through command line. 

> python UnCampTokenCountDemo.py tokencount.zip 
This demo sends Solr query string ["XXX"] to Solr proxy, extracts volume id from XML returned, sends the volume id list to Data API to get token count of the volumes and finally saves the results in a zip file whose name is provided through command line.

6.	View the results. Each demo should create one zip file. UnCampVolumeDemo.py creates a zip file with [some number] folders. Each folder uses a volume id as its name and contains all the page contents as separated files. UnCampTokenCountDemo.py creates a zip file with [some number] text files. Each text file uses a volume id as its name and has the token count for that volume. 

7.	You can change the requests sent to Data API/Solr by tweaking the parameters defined in configuration.py. There are two sets of parameters you can tweak for the demos. One is Data API parameters. The other one is Solr parameters. 

7.1	Tweak VOLUME_PARAMETERS for Data API. 
Change it as follows and rerun UnCampVolumeDemo.py in step 5.
VOLUME_PARAMETERS = {'mets' : 'true'}
This allows Data API to return mets record along with the volume content.

Change VOLUME_PARAMETERS again as follows and rerun UnCampVolumeDemo.py in step 5.
VOLUME_PARAMETERS = {'mets' : 'true', 'concat' : 'true'}
This allows Data API to return mets record along with the volume content and concatenate all the pages into one single text file per volume.

7.2	Tweak TOKENCOUNT_PARAMETERS for Data API. 
Change it as follows and rerun UnCampTokenCountDemo.py in step 5.
TOKENCOUNT_PARAMETERS = {'level' : 'page', 'sortBy' : 'count', 'sortOrder' : 'asc'} 
This allows Data API to return token count in page level and sort the result by count in ascending order.   

7.3 Tweak Solr parameters

