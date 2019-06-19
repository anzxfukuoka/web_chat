from flask import Flask
from flask import abort, redirect, url_for, render_template
from flask import session, escape, request

from flask_socketio import SocketIO
from flask_socketio import send, emit

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

socketio = SocketIO(app)

@app.route("/index")
def index():
    return redirect('/')

@app.route("/")
def main():
    if 'username' in session:
        return render_template('index.html')#'Logged in as %s' % escape(session['username'])
    else:
        return redirect(url_for("login"))

#login/logout

@app.route("/login" , methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))



#chat
#js + socketio

#username, status(online/offline)
users = {}
#username, text
messages = {}

#проблемс:
#юзкр ушел со странички/разлогинелся, но все еще коннекткд

@socketio.on('message')
def handle_message(message):
    print(session["username"] + " : " + message)
    #send(json, json=True)
    #broadcasting
    json = {'username': session["username"], "text": message}
    emit('new message', json, broadcast=True)


@socketio.on('connect')
def on_connect():
    print(session["username"] + " connected")
    emit('new sys message', session["username"] + " connected", broadcast=True)
    pass

@socketio.on('disconnect')
def on_disconnect():
    print(session["username"] + " disconnected")
    emit('new sys message', session["username"] + " disconnected", broadcast=True)
    #timeout to delete from users
    pass


#tripcode

def gen_tripcode(password):
        random.seed(app.secret_key)#random.seed(password)
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
