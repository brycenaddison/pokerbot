import sys
import pymongo


class Database:

    def __init__(self, db, col, key=sys.argv[2]):
        """
        Creates a connection to the given database, allowing users to access data.
        :param db: The database you choose to access
        :param col: The collection you choose to access
        :param key: The login string for the database
        """
        self.client = pymongo.MongoClient(key, connect=False)
        self.collection_id = str(col)
        self.database = self.client[db]
        self.collection = self.database[self.collection_id]

    def __del__(self):
        """
        Closes the client on object destruction
        """
        self.client.close()

    def get_value(self, query_key, query_value, return_key):
        """
        Returns the value at a given key for an entry that matches the query
        :param query_key: The key used to identify the entry
        :param query_value: The value at the query key, used to identify the entry
        :param return_key: The key of the desired return value
        :return: The given value at return_key
        """
        query = {query_key: query_value}
        response = self.collection.find(query)
        return response[0][return_key]

    def new_entry(self, data):
        """
        Inserts a dict into the database
        :param data: A dict to be inserted into the database
        """
        self.collection.insert_one(data)

    def delete_entry(self, key, value):
        """
        Deletes an entry with the given key and value
        :param key: The identifying key
        :param value: The value of the identifying key for the entry to be deleted
        """
        data = {
            key: value
        }
        self.collection.delete_one(data)

    def is_there(self, key, value):
        """
        Returns a boolean value given by whether the given entry exists in the database
        :rtype: boolean
        :param key:  The identifying key
        :param value: The corresponding value
        :return: A boolean value as to whether the entry exists
        """
        query = {key: value}
        response = self.collection.find(query)
        if len(response) > 0:
            return True
        return False

    def set_value(self, key, value, data):
        """
        Updates the value of an entry
        :param key: The identifying key of the entry
        :param value: The identifying value of the entry
        :param data: The dict containing the key(s) to be updated and the values to update them with
        """
        query = {key: value}
        data = {"$set": data}
        self.collection.update_one(query, data)

    def find_all(self, key, value):
        """
        Returns all entries with matching key and value
        :rtype: list
        :param key: The identifying key
        :param value: The identifying value
        :return: A list of entries that match key and value
        """
        query = {key: value}
        response = self.collection.find(query)
        return response

    def add_value(self, query_key, query_value, key, value):
        """
        Adds a new value to an array.
        :param query_key: The identifying key
        :param query_value: The identifying value
        :param key: The key to update
        :param value: The value to add to the array
        """
        query = {query_key: query_value}

        try:
            new_entry = {"$push": {key: value}}
            self.collection.update_one(query, new_entry)
        except Exception as e:
            print(type(e))
            new_entry = {"$set_value": {key: []}}
            self.collection.update_one(query, new_entry)
            new_entry = {"$push": {key: value}}
            self.collection.update_one(query, new_entry)

    def remove_value(self, query_key, query_value, key, value):
        """
        Removes a value from an array
        :param query_key: The identifying key
        :param query_value: The identifying value
        :param key: The key to update
        :param value: The value to remove from the array
        """
        query = {query_key: query_value}

        new_entry = {"$pull": {key: value}}
        self.collection.update_one(query, new_entry)
