from django.conf import settings

import pymongo
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId
from json import JSONEncoder


def connect(collectionname):
    client_uri = settings.MONGO_URI
    data = {
        'errors': {},
        'connection': {}
    }

    client = None
    db = None
    collection = None
    try:
        client = pymongo.MongoClient(client_uri)
        db = client.appdb
        collection = db[collectionname]
    except ConnectionFailure:
        data['errors']['ConnectionFailure'] = 'Cannot connect to MongoDB server'
    finally:
        data['connection']['client'] = client
        data['connection']['db'] = db
        data['connection']['collection'] = collection

    return data


def getDocument(collectionname, filter):
    data = connect(collectionname)
    document = []

    if data['connection']['collection'] is None:
        return data['errors']

    if filter is not None:
        doc = data['connection']['collection'].find_one(filter)
    else:
        doc = data['connection']['collection'].find_one()
    doc.pop('_id')
    document.append(doc)

    return document


def insertDocument(collectionname, update_data):
    data = connect(collectionname)
    data['connection']['collection'].insert_one(update_data)

    return True


def updateDocument(collectionname, filter, update_data):
    data = connect(collectionname)
    document = []

    if filter is not None:
        doc = data['connection']['collection'].find_one(filter)
    else:
        doc = data['connection']['collection'].find_one()

    for k, v in update_data.items():
        doc[k] = v

    data['connection']['collection'].save(doc)

    doc.pop('_id')
    document.append(doc)

    return document
