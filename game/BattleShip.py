from game import GUI
from game.Board import Board
from game.EmptySea import EmptySea
from game.HorizontalShip import HorizontalShip
from game.VerticalShip import VerticalShip


def whichshiptocreate(size, allign):
    if allign == 0:
        return HorizontalShip(size)
    elif allign == 1:
        return VerticalShip(size)
    else:
        return EmptySea()


def game():
    ships = []
    xdim,ydim = GUI.askforboardsize()
    board = Board(xdim, ydim)
    GUI.printboard(board)
    while True:
        size, xpos, ypos, allign = GUI.askforshiptoplace()
        ship = whichshiptocreate(int(size), allign)
        if board.oktoplaceship(int(ypos), int(xpos), ship):
            board.placeshipat(int(ypos), int(xpos), ship)
            ships.append(ship)
        next = input("Would you like to continue providing ships yes/no = 1/0 respectively: ")
        if next.isdigit():
            if next == "0":
                break
            elif next == "1":
                continue
            else:
                print("Bad choose!")
                break
        else:
            print("Bad data. End of providing ships!")
    while len(ships) > 0:
        row, col = GUI.wheretoshot()
        _, text = board.shootat(row, col)
        print(text)
        GUI.printboard(board)
        if "sink" in text:
            ships.pop()
            print("Congratulations you sink all the ships! Game over! ")

game()


