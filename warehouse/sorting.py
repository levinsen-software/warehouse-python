class Sorting():
    def __init__(self, sort, order, key):
        self.sort = sort
        self.order = order
        self.key = key
    
    def as_dict(self):
        j = {
            "sort": self.sort,
            "order": self.order
        }

        if self.key != None:
            j["key"] = self.key

        return j