import os
import json
from google.cloud import storage
from google.cloud.storage import Blob
import google.cloud.exceptions
from gcloud_requests.connection import storage_http

class GCSService(object):
    """
    Wrapper for google cloud storage"
    """

    def __init__(self, config):
        self.project = config["project"]
        self.bucket = config["bucket"]
        self.client = storage.Client(project=self.project, _http = storage_http).get_bucket(self.bucket)
        
    
    def get_storage_location(self):
        """
        Get storage location for this Service
        :return: Google Cloud Storage bucket name
        """
        return self.bucket

    def put_object(self, key, data):
        """
        Put an object in Google Cloud Storage
        :param key: key of the object.
        :param data: data of the object
        :type data: str/bytes
        :return: None
        """
        Blob(key, self.client).upload_from_string(data)

    def get_object(self, key):
        """
        Get object from GCS with a key.
        :param key: key of the object
        :return: Data of the object
        :rtype: str/bytes
        """
        return Blob(key, self.client).download_as_string()

    def get_callset_status(self, callset_prefix, status_suffix = "status.json"):
        """
        Get status for a prefix.
        :param callset_prefix: A prefix for the callset.
        :param status_suffix: Suffix used for status files. By default, "status.json"
        :return: A list of call IDs
        """
        paginator = self.client.list_blobs(prefix = callset_prefix)
        status_keys = []
        for blob in paginator:
            if str.endswith(str(blob.name), status_suffix):
                status_keys.append(blob.name)
        call_ids = [k[len(callset_prefix) + 1:].split("/")[0] for k in status_keys]
        return call_ids
                

    def get_call_status(self, status_key):
        """
        Get the status for a call.
        :param status_key: status key
        :return: Updated status if status key exists, otherwise None.
        """
        try:
            data = self.get_object(status_key)
            return json.loads(data.decode('ascii'))
        except google.cloud.exceptions.NotFound as e:
            return None

    def get_call_output(self, output_key):
        """
        Get the output for a call.
        :param output_key: output key
        :return: output for a call, throws exception if output key does not exist
        """
        return self.get_object(output_key)
