from azure.storage.blob import BlockBlobService
import os
from requests import put
import zipfile

# Fetch runtime
condaruntime_binary = BlockBlobService(
      account_name="apengwin",
      account_key=None
    ).get_blob_to_bytes(
      "pywren",
      "Miniconda2.tar.gz",
    )

#deploy.
FUNCTION_NAME = {}
BASEURL = "https://{}.scm.azurewebsites.net".format(FUNCTION_NAME)

PUT_URL = BASEURL + "api/zip/site/wwwroot/conda"

KUDU_USER= ""
KUDU_PASS = ""

file_like_object = io.BytesIO()
zipfile_obj = zipfile.ZipFile(file_like_object, mode='w')

zipfile_obj.writestr("condaruntime.tar.gz", condaruntime_binary)
zipfile_obj.write("./extract.py")

zipfile_obj.close()

r = put(PUT_URL, auth=(KUDU_USER, KUDU_PASS), data=file_like_object.getvalue())

if r.status_code == 200:
    print("successfully put runtime")
else:
    print(r.status_code)
    print(r.text)

