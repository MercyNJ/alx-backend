#!/usr/bin/env python3
"""
LFUCache Module:caching system using the LFU algorithm.

This module defines the LFUCache class that inherits
from BaseCaching.
It includes methods for adding items to the cache (put),
retrieving items from the
cache (get), and managing the cache size based on
the Least Frequently Used (LFU) algorithm.
"""

from collections import defaultdict
from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """LFUCache class that inherits from
    BaseCaching and implements LFU algorithm."""
    def __init__(self):
        """
        Initialzation.
        """
        super().__init__()
        self.order = OrderedDict()
        self.frequency = {}

    def put(self, key, item):
        """
        Add item to cache.
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS \
                    and key not in self.cache_data.keys():
                least_freq_items = [k for k, v in self.frequency.items()
                                    if v == min(self.frequency.values())]

                discarded_key = min(
                        least_freq_items, key=lambda k: self.order[k])

                del self.cache_data[discarded_key]
                del self.frequency[discarded_key]
                del self.order[discarded_key]
                print("DISCARD: {}".format(discarded_key))

            self.cache_data[key] = item
            self.frequency[key] = self.frequency.get(key, 0) + 1
            self.order[key] = max(self.order.values(), default=-1) + 1

    def get(self, key):
        """
        Get item by its key.
        """
        if key is None or key not in self.cache_data:
            return None

        self.order[key] = max(self.order.values(), default=-1) + 1
        self.frequency[key] = self.frequency.get(key, 0) + 1

        return self.cache_data[key]
