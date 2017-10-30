from azure.storage.blob import BlockBlobService
import os
from requests import put

# Fetch runtime
BlockBlobService(
      account_name="apengwin",
      account_key=None
    ).get_blob_to_path(
      "pywren",
      "Miniconda2.tar.gz",
      "./condaruntime.tar.gz"
    )

#deploy.
r = put()
if r.status_code == 200:
    print("successfully deployed")
else:
    print(r.status_code)
    print(r.text)

