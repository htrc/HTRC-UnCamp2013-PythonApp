Steps below show you how to run the demo applications against HTRC Data API and HTRC Solr Proxy. The applications have been tested on Python 2.7.5.

1.	Get your client id and client secret from [URL]. Data API is protected by Oauth2 authetication. You need client id and client secret to access the Data API.

2.	Download the demo archive from [URL].

3.	Unzip the archive. You will see files "uncamputils.py", "UnCampVolumeDemo.py", and "UnCampTokenCountDemo.py" under folder "HTRC-UnCamp2013-PythonApp".

4.	Edit your client id and client secret in OAUTH2_CLIENT_ID and OAUTH2_CLIENT_SECRET defined in "UnCampVolumeDemo.py" or "UnCampPageDemo.py" or "UnCampTokenCountDemo.py". A sample setting is as follows.
OAUTH2_CLIENT_ID = "YOUR_CLIENT_ID"
OAUTH2_CLIENT_SECRET = "YOUR_CLIENT_SECRET"

5.	Run the demos by typing following command. Assume your command line terminal is under folder "HTRC-UnCamp2013-PythonApp".
> python UnCampVolumeDemo.py volume.zip
This demo sends Solr query string "title:war AND author:Bill" to Solr proxy to get a list of volume id, sends the volume id list to Data API to download contents of the volumes and finally saves the contents in a zip file whose name is provided through command line. 

> python UnCampPageDemo.py page.zip
This demo sends Solr query string "title:war AND author:Bill" to Solr proxy to get a list of volume id, append pape number after each volume id, sends the volume id list to Data API to download contents of the volumes and finally saves the contents in a zip file whose name is provided through command line. 

> python UnCampTokenCountDemo.py tokencount.zip 
This demo sends Solr query string "title:war AND author:Bill" to Solr proxy to get a list of volume id, sends the volume id list to Data API to get token count of the volumes and finally saves the results in a zip file whose name is provided through command line.

6.	View the results. Each demo app should create one zip file. UnCampVolumeDemo.py creates a zip file with some folders. Each folder uses a volume id as its name and contains all the page contents as separated files. UnCampPageDemo.py creates a zip file with page contents specified in request. UnCampTokenCountDemo.py creates a zip file with some text files. Each text file uses a volume id as its name and has the token count for that volume. 

7.	You can change the requests sent to Data API/Solr Proxy by tweaking the parameters defined in UnCampVolumeDemo.py or UnCampPageDemo.py or UnCampTokenCountDemo.py. The parameters are defined near the top of the file, before any class and functions. There are two sets of parameters you can tweak for the demos. One is Data API parameters. The other one is Solr parameters. 


