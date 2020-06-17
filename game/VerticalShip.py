from game.Ship import Ship


class VerticalShip(Ship):

    def __init__(self, size):
        super().__init__(size)
        self._isHorizontal = False

    def shootat(self, row, _):
        if self._row <= row <= self._row + self.getsize() - 1:
            if not self._hit[row - self._row]:
                self._hit[row - self._row] = True
                if not self.issunk():
                    self._shipsymbols[row - self._row] = self.hitted_ship_symbol
                    return True, "Hit!"
                else:
                    for i in range(0, len(self._shipsymbols)):
                        self._shipsymbols[i] = self.sunked_ship_symbol
                    print()
                    return True, "Hit and sink %s" % (self.getshiptype())
            else:
                return False, "You already shot there!"
        else:
            print()
            return False, "You gave wrong row!"


    def tostring(self, row, column):
        if self.issunk():
            return Ship.sunked_ship_symbol
        else:
            return self._shipsymbols[row - self._row]

    def getishorizontal(self):
        return self._isHorizontal
