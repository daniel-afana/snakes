
import time

from collections        import deque
from random             import randint

from flask              import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room
from flask_socketio import leave_room, close_room, rooms
from flask_socketio import disconnect

from snake import GSnake
from snake import DIRECTIONS
from point import GPoint

from copy import deepcopy

async_mode = None

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app, async_mode=async_mode)

thread = None

tick            = 0.3
app.paused      = True

snakes = {}

# def remove_snake(private_key):
#     del snakes[private_key]

def create_snake(username):
    b = deque()
    x = randint(4,45)
    y = randint(4,45)
    b.appendleft(GPoint(x=x, y=y))
    b.appendleft(GPoint(y=y + 1))
    b.appendleft(GPoint(y=y + 2))
    snake = GSnake(b)
    snakes[username] = snake

def restart_game():
    app.paused = False
    background_thread()

def game_over(key):
    del snakes[key]
    socketio.emit("game_over", namespace="/test")
    print('game over')


def background_thread():

    GSnake.generate_apple()

    while True:

        socketio.sleep(tick)
        if not app.paused:
            [s.MakeStep() for s in snakes.values()]
        
        over = []
        for k,v in snakes.items():
            dc = deepcopy(snakes)
            del dc[k]
            if v.hit_border or v._bite_self or v.bite_somebody(dc.values()):
                over.append(k)
        for k in over:
            game_over(k)
        over.clear()

        response = {}
        response["snakes"] = list(map(lambda s: s.GetAsDict(), snakes.values()))
        response["apple"] = {"x":GSnake.apple.x, "y":GSnake.apple.y}
        socketio.emit(
            "field_change",
            response,
            namespace="/test"
        )



@app.route("/")
def index():
    return render_template("index.html")


@socketio.on('new player', namespace='/test')
def new_player(message):
    if message['data'] in snakes.keys():
        emit('username is already taken')
    create_snake(message['data'])
    # session['keyo'] = request.args.get('session')
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=restart_game)
    # emit('my response',
    #     {'data': message['data'], 'count': session['receive_count']})


@socketio.on("turn up", namespace="/test")
def turn_up(message):
    snakes[message['data']].ChangeDirection(DIRECTIONS.UP)


@socketio.on("turn right", namespace="/test")
def turn_right(message):
    snakes[message['data']].ChangeDirection(DIRECTIONS.RIGHT)


@socketio.on("turn left", namespace="/test")
def turn_left(message):
    snakes[message['data']].ChangeDirection(DIRECTIONS.LEFT)


@socketio.on("turn down", namespace="/test")
def turn_down(message):
    snakes[message['data']].ChangeDirection(DIRECTIONS.DOWN)


@socketio.on("toggle pause", namespace="/test")
def pause(message):
    print("poop")
    app.paused = not app.paused


@socketio.on("restart_game", namespace="/test")
def restart(message):
    restart_game()


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('prompt username')
    

# @socketio.on('disconnect', namespace='/test')
# def disconnect():
#     game_over(session['keyo'])



if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=8000)
