from requests import put
import os
import io
import zipfile
from azure.storage.queue import QueueService


FUNCTION_NAME = "allanepngfoobar"

BASEURL = "https://functionsef752afe.scm.azurewebsites.net/".format(FUNCTION_NAME)

PUT_URL = BASEURL + "/api/zip/site/wwwroot"

USER = "apengwin@berkeley.edu"
PASS = ""
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))

file_like_object = io.BytesIO()
zipfile_obj = zipfile.ZipFile(file_like_object, mode='w')

for f in ['function.json', 'run.py', 'jobrunner.py',
          '../version.py']:
    f = os.path.abspath(os.path.join(SOURCE_DIR, f))
    a = os.path.relpath(f, SOURCE_DIR + "/..")

    zipfile_obj.write(f, arcname=a)
zipfile_obj.writestr("host.json", "{}")

zipfile_obj.close()

r = put(PUT_URL, auth = (USER, PASS), data=file_like_object.getvalue())
print r
print "funciion deployed"

queue_service = QueueService(account_name='myaccount', account_key='mykey')
queue_service.create_queue("pywrenqueue")

print "queue deployed"
