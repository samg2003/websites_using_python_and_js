import os

from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
from flask_session import Session
from datetime import datetime

app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

messages = {};channels = [];usernames = []

@app.route("/check")
def check():
    return {'messages':messages, 'channels':channels, 'usernames':usernames}



@app.route("/")
def index():
    if "username" in session:
        if "channelname" in session:
            if len(messages.keys()) >= session["channelname"]:
                return redirect(url_for('chatroom', channelname=session["channelname"]))
            else:
                return redirect(url_for('channelslist'))
        else:
            return redirect(url_for('channelslist'))
    else:
        return render_template("index.html")



@app.route("/channels", methods=["GET", "POST"])
def channelslist():
    if request.method == "POST":
        username = request.form.get("username")
        if username in usernames:
            return render_template("error.html", message="Username is already taken", link="/")
        else:
            session["username"] = username
            usernames.append(username)

    if request.method == "GET":
        if "username" not in session:
            return render_template("error.html", message="Welcome.. it seems you have not entered your username", link='/')

    return render_template("channels.html", channels=channels, username=session["username"])



@app.route("/logout", methods=["GET"])
def logout():

    # Removing username from username list and from session
    try:
        temp = session.pop("username")
    except KeyError:
        return render_template("error.html", message="Welcome.. it seems you have not entered your username", link ='/')
    else:
        if temp in usernames:
            usernames.remove(temp)
    return redirect(url_for('index'))

@socketio.on("add message")
def message(data):
    selection = data["selection"]
    time = datetime.now().strftime("%d-%B-%Y %H:%M")
    _message = {"username": session["username"],"selection": selection, "time": time}
    messagelist = messages[channels[session["channelname"] - 1]]
    if len(messagelist) > 100:
        del messagelist[:len(messagelist)-100]
    messagelist.append(_message)
    emit("display mess", {**_message, **{"channelname": str(session["channelname"])}}, broadcast=True)


@socketio.on("add channel")
def add_channel(data):
    emit("display chan", {"selection": data["selection"], "channelname": len(channels)+1}, broadcast=True)


@app.route("/messagesload", methods=["POST"])
def messagesload():
    return jsonify({**{"message": messages[channels[session["channelname"]-1]]}, **{"channelname": session["channelname"]}})



@app.route("/channels/<int:channelname>", methods=["GET", "POST"])
def chatroom(channelname):

    if request.method == "POST":
        channelid = request.form.get("channelName")
        if channelid in messages.keys():
            return render_template("error.html", message="The chatroom already exists. you can either join the channel or create with different name", link="/channels")
        channels.append(channelid)
        messages[channelid] = []

    if request.method == "GET":
        if "username" not in session:
            return render_template("error.html", message = "Welcome.. it seems you have not entered your username", link = "/")
        elif len(messages.keys()) < channelname:
            return render_template("error.html", message="no such chatroom exists... but you can always create new one", link = "/channels")

    session["channelname"] = channelname

    return render_template("chatroom.html", username=session["username"])
