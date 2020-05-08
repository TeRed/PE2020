import json


class ArticleLogs:

    def __init__(self, id, logs):
        self.id = id
        self.logs = logs

    def __eq__(self, other):
        return self.id == other.id and self.logs == other.logs

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


