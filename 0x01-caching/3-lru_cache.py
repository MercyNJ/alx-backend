#!/usr/bin/env python3
"""
Create an LRUCache class inheriting from BaseCaching
with a cache dictionary self.cache_data.
Implement put to add items, discarding the
least recently used if the cache is full. The get method returns
the value for a key, updating its usage.
"""

from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """
    A LRUCache class that inherits from BaseCaching.
    """

    def __init__(self):
        """
        Initialize LRUCache.
        """
        super().__init__()
        self.order = OrderedDict()

    def put(self, key, item):
        """
        Add an item in the cache.
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS \
                    and key not in self.cache_data.keys():
                discarded_key, _ = self.order.popitem(last=False)
                del self.cache_data[discarded_key]
                print("DISCARD: {}". format(discarded_key))

            self.cache_data[key] = item
            self.order[key] = True

    def get(self, key):
        """
        Get an item by its key.
        """
        if key is None or key not in self.cache_data:
            return None

        self.order.move_to_end(key)

        return self.cache_data[key]
