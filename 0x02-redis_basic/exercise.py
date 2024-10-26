#!/usr/bin/env python3
'''A class for Cache using redis'''
import redis
import uuid
from typing import Union


class Cache():
    '''the Cache class with redis'''
    def __init__(self):
        '''initiates the class'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''store the input data in Redis using the random key and
        return the key.'''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
