from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)


@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!'})


if __name__ == '__main__':
    socketio.run(app, port=6001)
