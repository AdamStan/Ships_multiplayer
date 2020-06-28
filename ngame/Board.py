from random import randrange

from game.Board import Board
from game.Ship import Ship
from game.VerticalShip import VerticalShip
import json

BOARD_LENGTH = 5
BOARD_WIDTH = 5

BATTLESHIPS = 1
CRUISER = 2
DESTROYER = 3
SUBMARINE = 3

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
        # TODO: better ship initialization
        self.set_battleships(BATTLESHIPS)

    def set_battleships(self, how_many):
        ship_size = Ship.ShipType.BATTLESHIP.value
        for i in range(how_many):
            x = randrange(BOARD_LENGTH - ship_size)
            y = randrange(BOARD_WIDTH)
            self.placeshipat(x, y, VerticalShip(ship_size))

    def fields_to_json(self):
        dict_json = {}
        for row in range(0, len(self.getships())):
            for column in range(0, len(self.getships()[row])):
                dict_json[LETTERS_MAP[row] + str(column)] = self.getships()[row][column].tostring(row, column)
        return json.dumps(dict_json)

    def fields_to_json_hide(self):
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
        return json.dumps(dict_json)
