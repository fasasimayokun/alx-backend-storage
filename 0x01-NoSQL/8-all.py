#!/usr/bin/env python3
"""module that list all documents in Python """


def list_all(mongo_collection):
    """a func that lists all the documents in a collection"""
    if not mongo_collection.find({}).alive:
        return []
    return mongo_collection.find()
