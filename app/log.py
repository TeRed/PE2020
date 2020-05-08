import json


class Log:

    def __init__(self, id, data, text):
        self.id = id
        self.data = data
        self.text = text

    def __eq__(self, other):
        return self.id == other.id and self.data == other.data and self.text == other.text

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


