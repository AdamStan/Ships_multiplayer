from game.Ship import Ship


class HorizontalShip(Ship):

    def __init__(self, size):
        super().__init__(size)
        self._isHorizontal = True

    def shootat(self, _, column):
        """
        :param _:
        :param column:
        :return: True if coordinates are correct and True if ship was hit
        """
        if self._column <= column <= self._column + self.getsize() - 1:
            if not self._hit[column - self._column]:
                self._hit[column - self._column] = True
                if not self.issunk():
                    self._shipsymbols[column - self._column] = self.hitted_ship_symbol
                    return True, True
                else:
                    for i in range(0, len(self._shipsymbols)):
                        self._shipsymbols[i] = self.sunked_ship_symbol
                    return True, True
            else:
                return False, "You already shot there!"
        else:
            return False, "You gave wrong row!"

    def tostring(self, row, column):
        if self.issunk():
            return Ship.sunked_ship_symbol
        else:
            return self._shipsymbols[column - self._column]

    def getishorizontal(self):
        return self._isHorizontal
