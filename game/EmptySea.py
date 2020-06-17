from game.Ship import Ship


class EmptySea(Ship):

    hittedemptyseasymbol = "O"

    def __init__(self):
        super().__init__(1)
        self._isHorizontal = True

    def tostring(self, row, column):
        if self.gethit()[0]:
            return self.getshipsymbols()[0]
        return "~"

    def shootat(self, row, column):
        if (self.getcolumn() <= column <= self.getcolumn() + self.getsize() - 1) or\
                (self.getrow() <= row <= self.getrow() + self.getsize() - 1):
            if not self.gethit()[column - self.getcolumn()]:
                self.gethit()[column - self.getcolumn()] = True
                self.getshipsymbols()[column - self.getcolumn()] = self.hittedemptyseasymbol
                return True, "You shoot in Sea!"
            else:
                return False, "You already shoot there !"
        else:
            return False, "You gave wrong shooting coordinates "