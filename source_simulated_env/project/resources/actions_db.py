import random

import pymongo
from bson.objectid import ObjectId


class MongoDBActions:
    """
    A class to perform actions in a MongoDB database, such as creating,
    updating, and deleting documents in a specific collection.

    Arguments and Attributes:
        - ``uri (str):`` The MongoDB connection URI.
        - ``database_name (str):`` The name of the database.
        - ``collection_name (str):`` The name of the collection where actions
        will be performed.
        - ``document (dict):`` The initial data to be used for creating or editing
        documents.
    """

    def __init__(
        self,
        uri: str,
        database_name: str,
        collection_name: str,
        document: dict,
    ):
        self.uri = uri
        self.database_name = database_name
        self.collection_name = collection_name
        self.document = document
        self.client = pymongo.MongoClient(self.uri)

    def get_random_document(self) -> ObjectId | None:
        """
        Attempts to retrieve a document in the provided collection and returns
        its ObjectId. If no document is returned, the value None is returned.

        Returns:
            - ``ObjectId`` or ``None``: The ObjectId of the retrieved document,
            or None if no document is found.
        """
        db = self.client[self.database_name]
        collection = db[self.collection_name]
        random_document = collection.find_one({}, {'_id': 1})
        self.client.close()
        if random_document:
            return random_document['_id']
        return None

    def create_document(self) -> ObjectId:
        """
        Creates a new document in the provided collection using the specified data.

        Inserts a new document into the collection using the data supplied during
        object initialization.

        Returns:
        - ``ObjectId``: The ObjectId of the created document.
        """
        db = self.client[self.database_name]
        collection = db[self.collection_name]
        data = self.document
        id = collection.insert_one(data)
        self.client.close()
        return id.inserted_id

    def update_document(
        self, percent_to_update: int = 10, default_quantity: int | None = None
    ) -> ObjectId:
        """
        Update a random document in the provided collection with new data.

        Args:
            - ``percent_to_update (int, optional):`` Percentage of keys to update
            in the document. Default is 10.

            - ``default_quantity (int, optional):`` Number of keys to update in the
            document.

        This method attempts to update a random document in the collection with new data
        while keeping the ObjectId unchanged. The update process involves modifying a
        specified percentage of the keys in the document (controlled by the `percent_to_update`)
        or a specific number of keys (controlled by `default_quantity`).

        If a random document is not found in the collection, the function does not perform any updates.

        Returns:
        - ``ObjectId``: The ObjectId of the manipulated document.
        """
        db = self.client[self.database_name]
        collection = db[self.collection_name]

        random_id = self.get_random_document()

        if not random_id:
            random_id = self.create_document()

        if random_id:
            random_document = collection.find_one({'_id': random_id})

            if random_document:
                document_keys = list(random_document.keys())
                document_keys.remove('_id')

                if default_quantity is None:
                    num_keys_to_update = (
                        len(document_keys) * percent_to_update // 100
                    )
                    num_keys_to_update = max(num_keys_to_update, 1)
                else:
                    num_keys_to_update = min(
                        default_quantity, len(document_keys)
                    )

                keys_to_update = random.sample(
                    document_keys, num_keys_to_update
                )

                update_data = {}

                for key in keys_to_update:
                    value_to_update = self.document.get(key)
                    update_data[key] = value_to_update

                collection.update_one(
                    {'_id': random_id}, {'$set': update_data}
                )

        self.client.close()
        return random_id

    def delete_document(self)-> ObjectId:
        """
        Deletes a random document from the provided collection.

        Attempts to delete a random document from the collection based on its ObjectId.
        If no random document is found, the function does not perform any deletion.

        Returns:
        - ``ObjectId``: The ObjectId of the manipulated document.
        """
        db = self.client[self.database_name]
        collection = db[self.collection_name]

        random_id = self.get_random_document()

        if not random_id:
            random_id = self.create_document()

        if random_id:
            collection.delete_one({'_id': random_id})

        self.client.close()
        return random_id
