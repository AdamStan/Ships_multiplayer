import socketio

from ngame.Shoot import Shoot
from server.server_variables import FIRST

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
    coor = coordinates.split(",")
    shoot = Shoot(coor[0], coor[1])
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


sio.connect('http://localhost:8080')
sio.emit(event='connect_to_game')


def choosing_game():
    game_or_join = input("New game/join n/j \n")
    if game_or_join == "n":
        sio.emit("create_new_game")
    elif game_or_join == "j":
        game_id = input("Provide game id to join\n")
        sio.emit("join_to_game", data=int(game_id))


if __name__ == '__main__':
    choosing_game()
    sio.wait()