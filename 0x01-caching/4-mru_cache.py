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
        """Initialize MRUCache."""
        super().__init__()
        self.used = []

    def put(self, key, item):
        """Add an item to the cache using MRU algorithm."""
        if key is not None and item is not None:
            self.cache_data[key] = item
            if key not in self.used:
                self.used.append(key)
            else:
                self.used.append(
                    self.used.pop(self.used.index(key)))
            if len(self.used) > BaseCaching.MAX_ITEMS:
                discarded = self.used.pop(-2)
                del self.cache_data[discarded]
                print(f'DISCARD: {discarded}')

    def get(self, key):
        """Retrieve an item from the cache."""
        if key is not None and key in self.cache_data:
            self.used.append(self.used.pop(self.used.index(key)))
            return self.cache_data.get(key)
        return None
