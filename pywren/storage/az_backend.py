from .exceptions import StorageNoSuchKeyError

class AZBackend(object):
    """
    Wrapper for Azure storage APIs.
    """

    def __init__(self, config):
        self.container = config["container"]
        
    def put_object(self, key, data):
        """
        Put an object in az storage.
        Override the object if the key already exists.
        :param key: key of the object.
        :param data: data of the object
        :type data: str/bytes
        :return: None
        """
        pass


    def get_object(self, key):
        """
        Get object from storage with a key.
        Throws StorageNoSuchKeyError if the given key does not exist.
        :param key: key of the object
        :return: Data of the object
        :rtype: str/bytes
        """
        pass

    def key_exists(self, key):
        """
        Check if a key exists.
        :param key: key of the object
        :return: True if key exists, False if not exists
        :rtype: boolean
        """
        pass

    def list_keys_with_prefix(self, prefix):
        """
        Return a list of keys for the given prefix.
        :param key: key of the object
        :return: True if key exists, False if not exists
        :rtype: A list of keys
        """
        pass
