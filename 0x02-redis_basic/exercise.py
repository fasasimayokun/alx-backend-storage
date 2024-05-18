#!/usr/bin/env python3
""" module for Redis basic """
from functools import wraps
import typing
import uuid
import redis
from typing import Union, Optional, Callable, Any


def count_calls(method: Callable) -> Callable:
    """
    a func that count how many times methods of the Cache class are called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper content"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args)
    return wrapper


def call_history(method: Callable) -> Callable:
    """a func for storing lists"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper content"""
        key = method.__qualname__
        inpt = key + ":inputs"
        oupt = key + ":outputs"
        res = method(self, *args)
        self._redis.rpush(inpt, str(args))
        self._redis.rpush(oupt, res)
        return res
    return wrapper


def replay(method: Callable) -> None:
    """a func for retrieving lists for a particular function"""
    name = method.__qualname__
    client = redis.Redis()
    inputs = client.lrange("{}:inputs".format(name), 0, -1)
    outputs = client.lrange("{}:outputs".format(name), 0, -1)
    print("{} was called {} times:".format(name, len(inputs)))
    for ip, op in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(
                name, ip.decode("utf-8"), op.decode("utf-8")
            )
        )


class Cache():
    """a func that cache class definition"""

    def __init__(self):
        """the constructor method to Initialize redis instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes,  int,  float]) -> str:
        """
        a func that generates a random key using uuid,
        store the input data in Redis using the random key
        and return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """the get method to read from Redis and recovering original type"""
        element = self._redis.get(key)
        if not element:
            return None
        elif fn is int:
            return self.get_int(element)
        elif fn is str:
            return self.get_str(element)
        elif callable(fn):
            return fn(element)
        else:
            return element

    def get_str(self, data: bytes) -> str:
        """the methd to converts bytes to string"""
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """the method that converts bytes to integers"""
        return int(data)
