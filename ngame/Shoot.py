import json


class Shoot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def toJson(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.toJson()