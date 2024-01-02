#!/usr/bin/env python3
"""
A BasicCache module.
"""

BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """
    A BasicCache class that inherits from BaseCaching.
    """

    def __init__(self):
        """
        Initialiaze BasicCache.
        """
        super().__init__()

    def put(self, key, item):
        """
        Add an item in the cache.
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """
        Get an item by its key.
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
