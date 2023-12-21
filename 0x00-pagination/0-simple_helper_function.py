#!/usr/bin/env python3
"""
This module provides a function for calculating start
and end indexes for pagination.
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    calculates start index and an end index corresponding to the range of
    indexes to return in a list for those particular pagination
    parameters.
    """

    start_index: int = (page - 1) * page_size
    end_index: int = page * page_size
    return start_index, end_index
