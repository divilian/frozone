from flask import Flask, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, send
from pymongo import MongoClient
from datetime import datetime
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"
socketio = SocketIO(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["chatApp_test"]
rooms_collection = db.rooms

FRUIT_NAMES = ["apple", "banana", "blueberry", "strawberry", "orange", "grape", "cherry"]
TOPICS_LIST = ["Immigration", "Gun Control", "Climate Change Policy"]

def choose_names(n):
    # Return n unique random fruit names
    return random.sample(FRUIT_NAMES, n)

# Build the routes

@app.route('/', methods=["GET", "POST"])
def home():
    session.clear()
    if request.method == "POST":
        user_id = request.form.get('name')
        if not user_id:
            return render_template('home.html', error="Name is required")
        session['user_id'] = user_id
        return redirect(url_for('topics'))
    else:
        return render_template('home.html')

@app.route('/topics', methods=["GET", "POST"])
def topics():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('home'))
    return render_template('topics.html', topics=TOPICS_LIST)

@app.route('/choose', methods=["POST"])
def choose():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('home'))
    topic = request.form.get('topic')
    if not topic:
        return redirect(url_for('topics'))
    # Get next room id (and add one)
    counter = db.counters.find_one_and_update(
        {"_id": "room_id"},
        {"$inc": {"seq": 1}}, # increment seq by 1
        upsert=True, # create if missing
        return_document=True
    )
    room_id = counter["seq"]
    # Pick fruit display names
    fruit_names = choose_names(4)
    user_name = fruit_names[0]
    frobot_name = fruit_names[1]
    hotbot_name = fruit_names[2]
    coolbot_name = fruit_names[3]

    # Create the new room in the database
    rooms_collection.insert_one({
        "_id": room_id,
        "topic": topic,
        # creation date/time
        "created_at": datetime.utcnow(),
        # user identity
        "user_id": user_id,
        "user_name": user_name,
        # bot names
        "FroBot_name": frobot_name,
        "HotBot_name": hotbot_name,
        "CoolBot_name": coolbot_name,
        # empty message history
        "messages": [],
        # flag for if the user aborts
        "aborted": False
    })

    session['room'] = room_id
    session['display_name'] = user_name
    return redirect(url_for('room'))

@app.route('/room')
def room():
    room_id = session.get('room')
    display_name = session.get('display_name')
    if not room_id or not display_name:
        return redirect(url_for('home'))
    room_doc = rooms_collection.find_one({"_id": room_id})
    if not room_doc:
        return redirect(url_for('home'))
    return render_template("room.html", room=room_id, topic=room_doc["topic"], user=display_name, messages=room_doc["messages"], FroBot_name=room_doc["FroBot_name"], HotBot_name=room_doc["HotBot_name"], CoolBot_name=room_doc["CoolBot_name"])

@app.route("/abort", methods=["POST"])
def abort_room():
    room_id = session.get("room")
    if not room_id:
        return ("Error: No room in session.", 400)
    rooms_collection.update_one(
        {"_id": room_id},
        {"$set": {"aborted": True}}
    )
    return ("OK", 200)

# Build the SocketIO event handlers

@socketio.on('connect')
def handle_connect():
    name = session.get('display_name')
    room = session.get('room')
    if not name or not room:
        return
    join_room(room)
    send({
        "sender": "",
        "message": f"{name} has entered the chat"
    }, to=room)

@socketio.on('message')
def handle_message(payload):
    room = session.get('room')
    name = session.get('display_name')
    if not room or not name:
        return
    text = payload.get("message", "").strip()
    if not text:
        return  # ignore empty messages
    
    # Client-visible message (no datetime)
    client_message = {
        "sender": name,
        "message": text
    }
    # Database-only message (with datetime)
    db_message = {
        "sender": name,
        "message": text,
        "timestamp": datetime.utcnow()
    }
    # Send only the client version (no datetime)
    send(client_message, to=room)
    # Store the full version in the database
    rooms_collection.update_one(
        {"_id": room},
        {"$push": {"messages": db_message}}
    )

@socketio.on('disconnect')
def handle_disconnect():
    room = session.get("room")
    name = session.get("display_name")
    
    if room:
        send({
            "sender": "",
            "message": f"{name} has left the chat"
        }, to=room)
        leave_room(room)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

