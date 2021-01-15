from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin
from detect_finger import detect_finger

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app, cors_allowed_origins='*')


@socketio.on('connect')
def on_connect():
    while True:
        data = detect_finger()
        if data['type'] == 'FINGERPRINT_FOUND':
            emit('fingerprint', data)
            break
        else:
            print(data['type'])
            continue


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=6001)
