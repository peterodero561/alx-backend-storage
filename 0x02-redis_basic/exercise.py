#!/usr/bin/env python3
'''A class for Cache using redis'''
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''counts how many times a methods is called'''
    @wrapper(method)
    def wrapper(self, *args, **kwargs):
        '''helper function'''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs for a particular function."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output

    return wrapper


class Cache():
    '''the Cache class with redis'''
    def __init__(self):
        '''initiates the class'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
