from game import GUI
from ngame.Board import BoardExtended


class Game:

    def __init__(self, id):
        self.id = id
        self.socket_player_1 = None
        self.socket_player_2 = None
        self.board1 = BoardExtended()
        self.board2 = BoardExtended()

    def is_game_ready(self):
        return self.socket_player_1 is not None and self.socket_player_2 is not None

    def lets_shoot(self, sid, x, y):
        # TODO: adding checking if game was over (all ships are destroyed)
        if self.socket_player_1 == sid:
            values_to_return = self.board2.shootat(x, y)
        else:
            values_to_return = self.board1.shootat(x, y)
        print("Board 1")
        GUI.printboard(self.board1)
        print("Board 2")
        GUI.printboard(self.board2)
        return values_to_return
