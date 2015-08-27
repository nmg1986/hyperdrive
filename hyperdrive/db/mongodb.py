__author__ = 'nmg'


__all__ = ['MongoAPI']

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from hyperdrive.common import log as logging
import sys
import time


logger = logging.getLogger(__name__)


class MongoAPI(object):
    def __init__(self, host, port, db):
        self.host = host
        self.port = int(port)
        self.db = db
        self.connection = None
        self.max_retries = 5
        self.retry_interval = 5

        self.connect()

    def connect(self):
        attempt = 0
        while True:
            attempt += 1
            try:
                self._connect()
                logger.info("Connecting to MongoDB server on {}:{} succeed".format(self.host, self.port))
                return
            except ConnectionFailure:
                logger.error("Connecting to MongoDB failed...retry after {} seconds".format(self.retry_interval))

            if attempt >= self.max_retries:
                logger.error("Connecting to MongoDB server on {}:{} falied".format(self.host, self.port))
                sys.exit(1)
            time.sleep(self.retry_interval)

    def _connect(self):
        self.connection = MongoClient(self.host, self.port)

    def add_item(self, item, coll='items'):
        """
        Insert items in collection.

        @param coll: the collection, default to `items`
        @param msg: the items be saved

        @return: a WriteResult object that contains the status of the operation(not used currently)
        """
        coll = self.connection[self.db][coll]

        return coll.insert(item)

    def get_items(self, invent='items'):
        """
        Get items from collection.

        @param invent: the collection

        @return: `pymongo.cursor.Cursor object`
        """

        coll = self.connection[self.db][invent]

        return coll.find({})

    def get_item(self,  id, invent='items'):
        """
        Get specified item according item id.

        @param invent: the item table
        @param id: the item id

        @return: `pymongo.cursor.Cursor object`
        """
        coll = self.connection[self.db][invent]

        return coll.find_one({'id': id})

    def delete_item(self, id, invent='items'):
        """
        Delete item according item id.
        @param id: the item id
        @param invent: the item table
        """
        coll = self.connection[self.db][invent]

        return coll.remove({'id': id})

    def update_item(self, id, data, invent='items'):
        """
        Update item information.
        @param data:
        @param invent:
        """
        query = {'id': id}
        update = {'$set': data}

        coll = self.connection[self.db][invent]

        return coll.update(query, update)