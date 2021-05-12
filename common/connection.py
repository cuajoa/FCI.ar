from pymongo import MongoClient

_host='192.168.22.94'
_port=27017

class MongoDB(object):
    def __init__(self, database_name = 'fciar', collection_name = None):
        try:
            self._connection = MongoClient(host = _host, port = _port, maxPoolSize = 200)
        except Exception as error:
            raise Exception(error)
        self._database = None
        self._collection = None
        if database_name:
            self._database = self._connection[database_name]
        if collection_name:
            self._collection = self._database[collection_name]

    def getCollection(collection_name):
        mongo_db = MongoClient(host = _host, port = _port)
        db = mongo_db.fciar
        db_collection = db[collection_name]

        return db_collection
        
    def insert(self, post):
        # add/append/new single record
        post_id = self._collection.insert_one(post).inserted_id
        self._connection.close()
        return post_id