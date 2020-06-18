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
    await sio.emit("answer_on_new_game", data=game_id, room=sid)


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
        await sio.emit("next_shoot", room=game.socket_player_1)


@sio.event
async def shoot(sid, data):
    print("user wanna shot", sid)
    print("coordinates: ", data)
    game = find_game(sid)
    shoot_json = json.loads(data)
    correct_target, ship_hit = game.lets_shoot(sid, int(shoot_json['x']), int(shoot_json['y']))

    print(ship_hit)
    # TODO: add wining/losing game
    if game.socket_player_1 == sid:
        await choose_what_should_do(ship_hit=ship_hit, player_hit=game.socket_player_1, player_def=game.socket_player_2)
    elif game.socket_player_2 == sid:
        await choose_what_should_do(ship_hit=ship_hit, player_hit=game.socket_player_2, player_def=game.socket_player_1)


@sio.event
def disconnect(sid):
     # TODO: send information to user and remove game
    print('disconnect ', sid)


async def choose_what_should_do(ship_hit, player_hit, player_def):
    """
    :param ship_hit: true if ship was hit
    :param player_hit: player which shoot
    :param player_def: player which not shoot
    :return:
    """
    if ship_hit is True:
        await sio.emit("next_shoot", room=player_hit)
        await sio.emit("opponent_hit", room=player_def)
    else:
        await sio.emit("next_shoot", room=player_def)
        await sio.emit("answer_on_shoot", data="I gained your shot", room=player_hit)


def find_game(sid):
    for game in GAMES.values():
        if game.socket_player_1 == sid or game.socket_player_2 == sid:
            return game
    return Game(-1)


if __name__ == '__main__':
    web.run_app(app)
