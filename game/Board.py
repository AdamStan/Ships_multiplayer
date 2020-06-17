import copy

from game.EmptySea import EmptySea


class Board:

    def __init__(self, xdim, ydim):
        self.__xdimension = int(xdim)
        self.__ydimension = int(ydim)
        self.__ships = []
        for _ in range(0, self.__ydimension):
            extend_col = []
            for _ in range(0, self.__ydimension):
                extend_col.append(EmptySea())
            self.__ships.append(extend_col)

        for row in range(len(self.__ships)):
            for column in range(len(self.__ships[row])):
                self.__ships[row][column].setrow(row)
                self.__ships[row][column].setcolumn(column)

    def getxdim(self):
        return self.__xdimension

    def getydim(self):
        return self.__ydimension

    def isoccupied(self, row, column):
        if isinstance(self.__ships[row][column], EmptySea):
            return False
        else:
            return True

    def shootat(self, row, column):
        return self.__ships[row][column].shootat(row, column)

    def oktoplaceship(self, row, column, ship):
        k = 0
        if ship.getishorizontal():
            if column + ship.getsize() <= len(self.__ships[row]):
                for _ in range(ship.getsize()):
                    if not self.isoccupied(row, column):
                        k += 1
                        if k == ship.getsize():
                            return True
        else:
            if row + ship.getsize() <= len(self.__ships):
                for _ in range(ship.getsize()):
                    if not self.isoccupied(row,column):
                        k += 1
                        if k == ship.getsize():
                            return True
        print("This cell is occupied, use other,  ship is not placed !")
        return False

    def placeshipat(self, row, column, ship):
        if ship.getishorizontal():
            for i in range(ship.getsize()):
                self.__ships[row][column+i] = ship
            ship.setrow(row)
            ship.setcolumn(column)
        else:
            for i in range(0, ship.getsize()):
                self.__ships[row+i][column] = ship
            ship.setrow(row)
            ship.setcolumn(column)
        return True

    def getships(self):
        return copy.deepcopy(self.__ships)