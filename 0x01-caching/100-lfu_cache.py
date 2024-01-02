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
        """Initialize LFUCache."""
        super().__init__()
        self.frequency_counter = defaultdict(int)
        self.usage_order = OrderedDict()

    def put(self, key, item):
        """Add an item to the cache using LFU algorithm."""
        if key is not None and item is not None:
            self.cache_data[key] = item
            self.update_frequency_counter(key)
            self.manage_cache_size()

    def get(self, key):
        """Retrieve an item from the cache."""
        if key is not None and key in self.cache_data:
            self.update_frequency_counter(key)
            return self.cache_data[key]
        return None

    def update_frequency_counter(self, key):
        """Update the frequency counter and usage order for the given key."""
        self.frequency_counter[key] += 1
        if key in self.usage_order:
            del self.usage_order[key]
        self.usage_order[key] = None

    def manage_cache_size(self):
        """Manage the size of the cache based on LFU algorithm."""
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            least_frequent_keys = [k for k, v in self.frequency_counter.items()
                                   if v == min(self.frequency_counter.values())
                                   ]

            if len(least_frequent_keys) > 1:
                least_recently_used_key = min(
                        self.usage_order, key=lambda k: (
                            self.usage_order[k], k), default=None)
                discarded_key = least_recently_used_key
            else:
                discarded_key = least_frequent_keys[0]

            del self.cache_data[discarded_key]
            del self.frequency_counter[discarded_key]
            del self.usage_order[discarded_key]
            print('DISCARD: {:s}'.format(discarded_key))
