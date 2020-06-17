from unittest import TestCase

from game.Board import Board
from game.EmptySea import EmptySea
from game.HorizontalShip import HorizontalShip
from game.VerticalShip import VerticalShip


class TestBoard(TestCase):
    def setUp(self):
        self.board = Board(10, 10)
        self.horizontalShip = HorizontalShip(4)
        self.verticalShip = VerticalShip(3)

    def test_get_xdim(self):
        self.assertEqual(self.board.getxdim(), 10)

    def test_get_ydim(self):
        self.assertEqual(self.board.getydim(), 10)

    def test_is_occupied(self):
        self.assertEqual(self.board.isoccupied(5, 5), False)

    def test_shoot_at_empty_sea(self):
        self.assertEqual(self.board.shootat(4, 4), (True, "You shoot in Sea!"))

    def test_shoot_at_horizontal_ship(self):
        self.board.placeshipat(0, 0, self.horizontalShip)
        self.assertEqual(self.board.shootat(0, 0), (True, "Hit!"))

    def test_shoot_at_vertical_ship(self):
        self.board.placeshipat(0, 0, self.verticalShip)
        self.assertEqual(self.board.shootat(0, 0), (True, "Hit!"))

    def test_ok_to_place_ship(self):
        self.assertEqual(self.board.oktoplaceship(5, 5, self.verticalShip), True)

    def test_place_ship_at(self):
        self.assertEqual(self.board.placeshipat(3, 3, self.horizontalShip), True)

    def test_get_ships(self):
        k = 0
        for row in range(len(self.board.getships())):
            for column in range(len(self.board.getships()[row])):
                if isinstance(self.board.getships()[row][column], EmptySea):
                    k += 1
        self.assertEqual(self.board.getydim()*self.board.getxdim(), k)
