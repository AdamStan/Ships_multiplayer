from random import randrange

from game.Board import Board
from game.Ship import Ship
from game.VerticalShip import VerticalShip

BOARD_LENGTH = 5
BOARD_WIDTH = 5

BATTLESHIPS = 1
CRUISER = 2
DESTROYER = 3
SUBMARINE = 3


class BoardExtended(Board):
    def __init__(self):
        super().__init__(BOARD_LENGTH, BOARD_WIDTH)
        self.initialize_ship()

    def initialize_ship(self):
        self.set_battleships(BATTLESHIPS)

    def set_battleships(self, how_many):
        ship_size = Ship.ShipType.BATTLESHIP.value
        for i in range(how_many):
            x = randrange(BOARD_LENGTH - ship_size)
            y = randrange(BOARD_WIDTH)
            self.placeshipat(x, y, VerticalShip(ship_size))
