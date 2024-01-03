#!/usr/bin/env python3
"""
MRUCache Module

This module defines a MRUCache class
that inherits from BaseCaching.
It implements a caching system using the
Most Recently Used (MRU) algorithm.
"""

from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """MRUCache class that implements MRU algorithm."""
    def __init__(self):
        super().__init__()
        self.order = OrderedDict()

    def put(self, key, item):
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS \
                    and key not in self.cache_data.keys():
                discarded_key, _ = self.order.popitem(last=True)
                del self.cache_data[discarded_key]
                print("DISCARD: {}".format(discarded_key))

            self.cache_data[key] = item
            self.order[key] = True

    def get(self, key):
        if key is None or key not in self.cache_data:
            return None

        self.order.move_to_end(key)

        return self.cache_data[key]
