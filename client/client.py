import socketio
import json

from ngame.Shoot import Shoot
from server.server_variables import FIRST
from ngame.Board import LETTERS_MAP

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')


@sio.event
def disconnect():
    print('disconnected from server')


@sio.event
def answer_on_new_game(data):
    print("Your game id: ", data)
    print("Waiting for another user")


@sio.event
def answer_on_join(data):
    if data == 1:
        print("game not exists")
        choosing_game()
    elif data == 2:
        print("game is full")
        choosing_game()
    elif data == 0:
        print("You've joined to game.")


@sio.event
def start_game(data):
    if data == FIRST:
        print("Game started")
    else:
        print("Waiting for opponent's move")


@sio.event
def answer_on_shoot(answer):
    print("Answer: ", answer)
    print("Waiting for opponent's move")


@sio.event
def next_shoot():
    coordinates = input("Provide coordinates \n")
    shoot = Shoot(coordinates[0], coordinates[1])
    sio.emit(event="shoot", data=shoot.toJson())


@sio.event()
def opponent_hit():
    print("Opponent scored")
    print("Waiting for opponent's move")


@sio.event
def opponent_out():
    print("Your opponent left, game was closed")


@sio.event
def win():
    print("You win")


@sio.event
def lose():
    print("You lose")


@sio.event
def show_my_board(data):
    my_board = json.loads(data)
    print("My board")
    show_board(my_board)


@sio.event
def show_enemy_board(data):
    enemy_board = json.loads(data)
    print("Enemy board")
    show_board(enemy_board)


@sio.event
def show_boards(data):
    boards = json.loads(data)
    my_board = boards["my_board"]
    enemy_board = boards["enemy_board"]

    print("My board")
    show_board(my_board)

    print("Enemy board")
    show_board(enemy_board)


sio.connect('http://localhost:8080')
sio.emit(event='connect_to_game')


def choosing_game():
    game_or_join = input("New game/join n/j \n")
    if game_or_join == "n":
        sio.emit("create_new_game")
    elif game_or_join == "j":
        game_id = input("Provide game id to join\n")
        sio.emit("join_to_game", data=int(game_id))


def show_board(board_in_json):
    key_first_letter = None
    lines = []
    for key in board_in_json:
        if key[0] is not key_first_letter:
            key_first_letter = key[0]
            lines.append([])
        lines[-1].append(board_in_json[key])
    top_line = "    "
    for i in range(len(lines[0])):
        top_line += str(i) + "    "
    print(top_line)
    for i in range(len(lines)):
        print(LETTERS_MAP[i] + " " + str(lines[i]))


if __name__ == '__main__':
    choosing_game()
    sio.wait()