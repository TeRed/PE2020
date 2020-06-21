import json


class Article:

    def __init__(self, id, name, quantity, is_available):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.is_available = is_available

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.is_available == other.is_available and self.quantity == other.quantity

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


