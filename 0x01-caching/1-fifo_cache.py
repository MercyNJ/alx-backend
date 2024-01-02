#!/usr/bin/env python3
"""
A FIFOCache module.
iT  inherits from BaseCaching and is a caching system.
use self.cache_data - dictionary from the parent class BaseCaching
You can overload def __init__(self): but don’t
forget to call the parent init: super().__init__()
"""

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """
    A FIFOCache class that inherits from BaseCaching.
    """

    def __init__(self):
        """
        Intiliaze the class
        """
        super().__init__()

    def put(self, key, item):
        """
        Add an item in the cache.
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS \
                    and key not in self.cache_data.keys():
                discarded_key = next(iter(self.cache_data.keys()))
                del self.cache_data[discarded_key]
                print("DISCARD: {}". format(discarded_key))

            self.cache_data[key] = item

    def get(self, key):
        """
        Get an item by its key.
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
