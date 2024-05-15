#!/usr/bin/env python3
"""module that Change school topics """


def update_topics(mongo_collection, name, topics):
    """a func that changes all topics of a school document based on name"""
    mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})
