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

    data['connection']['client'].close()

    return document


def getDocuments(collectionname, filter):
    data = connect(collectionname)
    documents = []

    if filter is not None:
        docs = data['connection']['collection'].find(filter)
    else:
        docs = data['connection']['collection'].find()

    for doc in docs:
        doc.pop('_id')
        documents.append(doc)

    data['connection']['client'].close()

    return documents


def insertDocument(collectionname, update_data):
    data = connect(collectionname)
    data['connection']['collection'].insert_one(update_data)

    data['connection']['client'].close()

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

    data['connection']['client'].close()

    return document


def numDocuments(collectionname):
    data = connect(collectionname)
    data['connection']['client'].close()

    return data['connection']['collection'].count()
