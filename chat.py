import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, join_room, leave_room, send

import eventlet.wsgi
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Render the home page to enter a username and join a chat room."""
    if request.method == 'POST':
        username = request.form.get('username')
        room = request.form.get('room')
        session['username'] = username
        session['room'] = room
        return redirect('/chat')
    return render_template('index.html')

@app.route('/chat')
def chat():
    """Render the text (chat) room page."""
    username = session.get('username')
    room = session.get('room')
    if not username or not room:
        return redirect('/')
    return render_template('text.html', username=username, room=room)

@socketio.on('join')
def handle_join(data):
    """Handle a user joining a room."""
    username = data['username']
    room = data['room']
    join_room(room)
    send(f'{username} has joined the room.', to=room)

@socketio.on('message')
def handle_message(data):
    """Broadcast a message to the room."""
    room = session.get('room')
    send(f"{session['username']}: {data['msg']}", to=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
