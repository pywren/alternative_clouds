# This is the script to deploy the function to the Azure.


from requests import put
import os
import io
import zipfile
from azure.storage.queue import QueueService
from azure.storage.blob import BlockBlobService


FUNCTION_NAME = ""

# Azure storage account name and primary key. See the README.
AZURE_STORAGE_ACC_NAME = ""
AZURE_STORAGE_KEY = ""

#publish credentials
KUDU_USER = ""
KUDU_PASS = ""

BASEURL = "https://{}.scm.azurewebsites.net/".format(FUNCTION_NAME)

PUT_URL = BASEURL + "/api/zip/site/wwwroot"

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))

file_like_object = io.BytesIO()
zipfile_obj = zipfile.ZipFile(file_like_object, mode='w')

for f in ['function.json', 'run.py', 'jobrunner.py']:
    f = os.path.abspath(os.path.join(SOURCE_DIR, f))
    a = os.path.relpath(f, SOURCE_DIR + "/..")
    zipfile_obj.write(f, arcname=a)

zipfile_obj.writestr("host.json", "{}")

zipfile_obj.close()

r = put(PUT_URL, auth = (KUDU_USER, KUDU_PASS), data=file_like_object.getvalue())
print r.text
print "funciion deployed"

queue_service = QueueService(account_name=AZURE_STORAGE_ACC_NAME, account_key=AZURE_STORAGE_KEY)
queue_service.create_queue("pywrenqueue")

print "queue deployed"

blob_service = BlockBlobService(account_name=AZURE_STORAGE_ACC_NAME, account_key=AZURE_STORAGE_KEY)
blob_service.create_container("pywren1")

print "container created"

