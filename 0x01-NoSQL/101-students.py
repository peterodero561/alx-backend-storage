#!/usr/bin/env python3
'''function that returns all students sorted by average score:'''
from pymongo import MongoClient


def top_students(mongo_collection):
    '''returns all students sorted by average score'''
    formation = [
            {
                '$group': {'_id': 'name', 'average': {'$avg': '$score'}}
            },
            {
                '$sort': {'average': -1}
            }
            ]
    result = list(mongo_collection.aggregate(formation))
    return result
