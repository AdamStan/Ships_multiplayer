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

    def who_win_who_loose(self):
        """
        :return: winner and loser (yes, two results)
        """
        all_ships_destroyed1 = True
        for ship_list in self.board1.getships():
            for ship in ship_list:
                all_ships_destroyed1 = all_ships_destroyed1 and ship.issunk()

        all_ships_destroyed2 = True
        for ship_list in self.board2.getships():
            for ship in ship_list:
                all_ships_destroyed2 = all_ships_destroyed2 and ship.issunk()

        if all_ships_destroyed1:
            return self.socket_player_2, self.socket_player_1

        if all_ships_destroyed2:
            return self.socket_player_1, self.socket_player_2

        return None, None
