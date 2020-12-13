from pymongo import MongoClient

class MongoDB(object):
    def __init__(self, database_name='fciar', collection_name=None):
        try:
            self._connection = MongoClient(host='localhost', port=27017, maxPoolSize=200)
        except Exception as error:
            raise Exception(error)
        self._database = None
        self._collection = None
        if database_name:
            self._database = self._connection[database_name]
        if collection_name:
            self._collection = self._database[collection_name]

    def insert(self, post):
        # add/append/new single record
        post_id = self._collection.insert_one(post).inserted_id
        return post_id