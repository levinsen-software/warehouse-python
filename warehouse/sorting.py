"""Sorting module"""

from typing import Optional

class Sorting():
    """Object represents settings for sorting results"""

    def __init__(self, sort: Optional[str], order: Optional[str], key: Optional[str]):
        self.sort = sort
        self.order = order
        self.key = key

    def as_dict(self):
        """Returns a dict representation of object"""
        sorting_spec = {
            "sort": self.sort,
            "order": self.order
        }

        if self.key is not None:
            sorting_spec["key"] = self.key

        return sorting_spec
