#!/usr/bin/env python3
'''Python function that returns the list of school having a specific topic'''
from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
    '''returns the list of school having a specific topic'''
    result = list(mongo_collection.find({'topicis': topic}))
    school_names = [school['name'] for school in result]
    return school_names
