"""Sorting module"""


class Sorting():
    """Object represents settings for sorting results"""

    def __init__(self, sort, order, key):
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
