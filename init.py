from flask import Flask
from flask import abort, redirect, url_for, render_template
from flask import session, escape, request

from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask_socketio import join_room, leave_room

import os
import random
import string
from time import sleep
from threading import Thread

app = Flask(__name__)

app.secret_key = b'efd55366d48baed81238da8273f431b5d25efdf2'

socketio = SocketIO(app)

@app.route("/index")
def index():
    return redirect('/')

@app.route("/")
def main():
    if 'username' in session:
        return render_template('index.html')
    else:
        return redirect(url_for("login"))

#login/logout


@app.route("/login" , methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        tmp = request.form['username']
        tmp = tmp.split("#")

        #пустая строка
        #надабы пофиксить в js
        if tmp[0] == "":
            return render_template('login.html', error="имя не может быть пустым")

        #tripcode
        if len(tmp) == 2:
            username = tmp[0] + gen_tripcode(tmp[1])
        else:
            username = tmp[0]

        session['username'] = username #request.form['username']

        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/log')
def log():
    re = ""
    for msg in messages:
        re += msg['username'] + ": " + msg["text"] + "<br>"
    return re

#chat
#js + socketio

#username: [uid, uid, ...]
users = {}
#username, text
messages = []

@socketio.on('message')
def handle_message(message):
    print(session["username"] + " : " + message)
    #broadcasting
    if not session.get("username"):
        emit('not in chat', {})

    json = {'username': session["username"], "text": message}
    emit('new message', json, broadcast=True)
    messages.append(json)

@socketio.on('connect')
def on_connect():

    if users.get(session["username"]):
        users[session["username"]].append(request.sid) # + id потоков socketio
        print(session["username"] + "открыл новую вкладку/перезагрузил страницу")
    else:
        users.update({session["username"]: [request.sid]}) #был оффлайн, теперь онлайн
        print(session["username"] + "первый за долгое время раз подключился")

    for msg in messages:
        if not msg.get("username"):
            emit('new sys message', msg["text"], broadcast=True)
        else:
            json = {'username': msg['username'], "text": msg["text"]}
            emit('new message', json, broadcast=True)

@socketio.on('join')
def on_join(data):

    if len(users.get(session["username"])) > 1: #длинна списка id потоков socketio
        return #уже в чате, может с другой вкладки

    print(session["username"] + " joined")
    print(request.sid)
    emit('new sys message', session["username"] + " joined", broadcast=True)
    messages.append({"text": session["username"] + " joined"})


@socketio.on('leave')
def on_leave(data):
    print(session["username"] + " вышел")

    emit('new sys message', session["username"] + " left", broadcast=True)
    messages.append({"text": session["username"] + " left"})
    users.pop(session["username"])


@socketio.on('disconnect')
def on_disconnect():
    try:
        print(session["username"] + "пинг не прошел, поток закрывается")

        users[session["username"]].remove(request.sid)
        if len(users[session["username"]]) == 0:
            print("последний поток закрался, теперь " + session["username"] + " offline")

            emit('new sys message', session["username"] + " disconnected", broadcast=True)
            messages.append({"text": session["username"] + " disconnected"})
            users.pop(session["username"])
    except:
        pass


#tripcode

def gen_tripcode(password):
        random.seed(password)
        a=string.ascii_letters+string.digits+string.digits
        trip='!%s%s%s%s%s%s%s%s%s%s' % (random.choice(a),random.choice(a),random.choice(a),random.choice(a),random.choice(a),random.choice(a),random.choice(a),random.choice(a),random.choice(a),random.choice(a))
        return trip

#error handlers

@app.errorhandler(404)
def page_not_found(error):
    print(error)
    return render_template('error_page.html', error=error), error.code

@app.errorhandler(401)
def unauthorized(error):
    return render_template('error_page.html', error=error), error.code

@app.errorhandler(500)
def unauthorized(error):
    return render_template('error_page.html', error=error)


app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
