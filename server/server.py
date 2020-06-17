import json
from random import randrange

from aiohttp import web
import socketio

from ngame.Game import Game
from server_variables import GAME_IDS_RANGE, ANSWER_GAME_NOT_EXISTS, ANSWER_GAME_IS_FULL, FIRST, SECOND

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
GAMES = {}


@sio.event
def connect(sid, environ):
    print("connect ", sid)

@sio.event
async def create_new_game(sid):
    print("creating new game")
    game_id = randrange(GAME_IDS_RANGE)
    while GAMES.get(game_id) is not None:
        game_id = randrange(GAME_IDS_RANGE)
    game = Game(game_id)
    game.socket_player_1 = sid
    GAMES[game_id] = game
    await sio.emit("answer_on_new_game", data=game_id)


@sio.event
async def join_to_game(sid, game_id):
    print(sid)
    print("add to game: ", game_id)
    game = GAMES[game_id]
    if game is None:
        await sio.emit("answer_on_join", data=ANSWER_GAME_NOT_EXISTS, room=sid)
    elif game.is_game_ready():
        await sio.emit("answer_on_join", data=ANSWER_GAME_IS_FULL, room=sid)
    else:
        game.socket_player_2 = sid
        await sio.emit("answer_on_join", data=0, room=sid)
        await sio.emit("start_game", data=FIRST, room=game.socket_player_1)
        await sio.emit("start_game", data=SECOND, room=game.socket_player_2)
        await sio.emit("next_shot", room=game.socket_player_1)


@sio.event
async def shoot(sid, data):
    print("user wanna shot", sid)
    print("coordinates: ", data)
    game = find_game(sid)
    shoot_json = json.loads(data)
    game.lets_shoot(sid, int(shoot_json['x']), int(shoot_json['y']))

    if game.socket_player_1 == sid:
        await sio.emit("next_shot", room=game.socket_player_2)
    elif game.socket_player_2 == sid:
        await sio.emit("next_shot", room=game.socket_player_1)

    await sio.emit("answer_on_shoot", data="I gained your shot", room=sid)


def find_game(sid):
    for game in GAMES.values():
        if game.socket_player_1 == sid or game.socket_player_2 == sid:
            return game
    return Game(-1)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    web.run_app(app)