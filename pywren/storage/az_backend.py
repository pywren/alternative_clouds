from azure.storage.blob import BlockBlobService

from .exceptions import StorageNoSuchKeyError

class AZBackend(object):
    """
    Wrapper for Azure storage APIs.
    """

    def __init__(self, config):

        self.container = config["container"]
        self.block_blob_service = BlockBlobService(
            account_name=config["account"],
            account_key=config["key"]
        )
        
    def put_object(self, key, data):
        """
        Put an object in az storage.
        Override the object if the key already exists.
        :param key: key of the object.
        :param data: data of the object
        :type data: str/bytes
        :return: None
        """
        self.block_blob_service.create_blob_from_bytes(
            container_name = self.container,
            blob_name = key,
            blob = data
        )


    def get_object(self, key):
        """
        Get object from storage with a key.
        Throws StorageNoSuchKeyError if the given key does not exist.
        :param key: key of the object
        :return: Data of the object
        :rtype: str/bytes
        """
        try:
            r = self.block_blob_service.get
        except azure.common.AzureMissingResourceHttpError as e:
            raise StorageNoSuchKeyError(key)

    def key_exists(self, key):
        """
        Check if a key exists.
        :param key: key of the object
        :return: True if key exists, False if not exists
        :rtype: boolean
        """
        return self.block_blob_service.exists(self.container, key)

    def list_keys_with_prefix(self, pref):
        """
        Return a list of keys for the given prefix.
        :param key: key of the object
        :return: True if key exists, False if not exists
        :rtype: A list of keys
        """
        paginator = self.block_blob_service.list_blobs(
            container = self.container,
            prefix = pref
        )

