#!/usr/bin/env python3
'''A class for Cache using redis'''
import redis
import uuid
from typing import Union, Callable, Optional


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

    def get(
            self,
            key: str,
            fn: Optional[
                Callable[[bytes], Union[str, int, float, bytes]]] = None
            ) -> Optional[Union[str, int, float, bytes]]:
        ''' convert the data back to the desired format.'''
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Optional[str]:
        '''returns data in utf-8'''
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        '''returns data as int'''
        return self.get(key, int)
