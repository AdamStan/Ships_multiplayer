from random import randrange

from game.Board import Board
from game.Ship import Ship
from game.VerticalShip import VerticalShip

BOARD_LENGTH = 10
BOARD_WIDTH = 10

BATTLESHIPS = 1
CRUISERS = 2
DESTROYERS = 3
SUBMARINES = 3

LETTERS_MAP = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "H",
    8: "I",
    9: "J",
    10: "K",
    11: "L",
    12: "M",
    13: "N",
    14: "O"
}

VALUES_MAP = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
    "J": 9,
    "K": 10,
    "L": 11,
    "M": 12,
    "N": 13,
    "O": 14
}


class BoardExtended(Board):
    def __init__(self):
        super().__init__(BOARD_LENGTH, BOARD_WIDTH)
        self.initialize_ship()

    def initialize_ship(self):
        self.set_battleships(BATTLESHIPS)
        self.set_cruisers(CRUISERS)
        self.set_destroyers(DESTROYERS)
        self.set_submarines(SUBMARINES)

    def set_battleships(self, how_many):
        ship_size = Ship.ShipType.BATTLESHIP.value
        for i in range(how_many):
            x = randrange(BOARD_LENGTH - ship_size)
            y = randrange(BOARD_WIDTH)
            self.placeshipat(x, y, VerticalShip(ship_size))

    def set_cruisers(self, how_many):
        ship_size = Ship.ShipType.CRUISER.value
        self.init_ships(how_many, ship_size)

    def set_destroyers(self, how_many):
        self.init_ships(how_many, Ship.ShipType.DESTROYER.value)

    def set_submarines(self, how_many):
        self.init_ships(how_many, Ship.ShipType.SUBMARINE.value)

    def init_ships(self, how_many, ship_size):
        for i in range(how_many):
            while True:
                x = randrange(BOARD_LENGTH - ship_size)
                y = randrange(BOARD_WIDTH)
                cannot_add = False
                for i in range(x, x + ship_size):
                    ship = self.getships()[x][y]
                    ship_type = ship.getshiptype()
                    if ship_type != Ship.ShipType.EMPTYSEA.name:
                        cannot_add = True
                if cannot_add:
                    continue
                self.placeshipat(x, y, VerticalShip(ship_size))
                break


    def fields_to_dict(self):
        dict_json = {}
        for row in range(0, len(self.getships())):
            for column in range(0, len(self.getships()[row])):
                dict_json[LETTERS_MAP[row] + str(column)] = self.getships()[row][column].tostring(row, column)
        return dict_json

    def fields_to_dict_hide(self):
        dict_json = {}
        for row in range(0, len(self.getships())):
            for column in range(0, len(self.getships()[row])):
                ship_type = self.getships()[row][column].tostring(row, column)
                type = "-"
                if ship_type == "X" or ship_type == "H":
                    type = ship_type
                elif ship_type == "O":
                    type = "O"
                dict_json[LETTERS_MAP[row] + str(column)] = type
        return dict_json
