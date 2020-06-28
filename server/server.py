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
        await send_boards(game)
        await sio.emit("next_shoot", room=game.socket_player_1)


@sio.event
async def shoot(sid, data):
    print("user wanna shot", sid)
    print("coordinates: ", data)

    game = find_game(sid)
    if game is None:
        return

    shoot_json = json.loads(data)
    correct_target, ship_hit = game.lets_shoot(sid, shoot_json['x'], int(shoot_json['y']))

    print(ship_hit)
    await send_boards(game)

    if await game_can_be_finished(game):
        return

    if game.socket_player_1 == sid:
        await choose_what_should_do(ship_hit=ship_hit, player_hit=game.socket_player_1, player_def=game.socket_player_2)
    elif game.socket_player_2 == sid:
        await choose_what_should_do(ship_hit=ship_hit, player_hit=game.socket_player_2, player_def=game.socket_player_1)


@sio.event
async def disconnect(sid):
    print('disconnect ', sid)
    game = find_game(sid)
    print("game to remove: ", game)
    if game is not None:
        if game.socket_player_1 == sid and game.socket_player_2 is not None:
            await sio.emit(event="opponent_out", room=game.socket_player_2)

        if game.socket_player_2 == sid and game.socket_player_1 is not None:
            await sio.emit(event="opponent_out", room=game.socket_player_1)

        GAMES.pop(game.id)


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


async def game_can_be_finished(game):
    winner, looser = game.who_win_who_loose()
    if winner is None:
        return False
    await sio.emit(event="win", room=winner)
    await sio.emit(event="lose", room=looser)
    return True


async def send_boards(game):
    board_1 = game.board1.fields_to_dict()
    board_1_hidden = game.board1.fields_to_dict_hide()
    board_2 = game.board2.fields_to_dict()
    board_2_hidden = game.board2.fields_to_dict_hide()
    player_one_data = json.dumps({"enemy_board": board_2_hidden, "my_board": board_1})
    player_two_data = json.dumps({"enemy_board": board_1_hidden, "my_board": board_2})

    await sio.emit(event="show_boards", data=player_one_data, room=game.socket_player_1)
    await sio.emit(event="show_boards", data=player_two_data, room=game.socket_player_2)


def find_game(sid):
    for game in GAMES.values():
        if game.socket_player_1 == sid or game.socket_player_2 == sid:
            return game
    return None


if __name__ == '__main__':
    web.run_app(app)
