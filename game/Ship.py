import enum
from abc import abstractmethod


class Ship:

    class ShipType(enum.Enum):
        BATTLESHIP = 4
        CRUISER = 3
        DESTROYER = 2
        SUBMARINE = 1
        EMPTYSEA = 0

        def __str__(self):
            return self.name

    sunked_ship_symbol = "X"
    hitted_ship_symbol = "H"

    @abstractmethod
    def __init__(self, size):
        self._row = 0
        self._column = 0
        self._size = size
        self._hit = []
        self._ishorizontal = True
        self._shipsymbols = []
        self._shiptype = Ship.ShipType(size).name
        for _ in range(size):
            self._hit.append(False)
            self._shipsymbols.append(str(size))

    def setrow(self, row):
        self._row = row

    def setcolumn(self, column):
        self._column = column

    def getsize(self):
        return self._size

    def getrow(self):
        return self._row

    def getcolumn(self):
        return self._column

    def getshipsymbols(self):
        return self._shipsymbols

    def gethit(self):
        return self._hit

    def getshiptype(self):
        return self._shiptype

    def issunk(self):
        if False in self._hit:
            return False
        else:
            return True