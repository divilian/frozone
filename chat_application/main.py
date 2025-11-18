from flask import Flask, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, send
from pymongo import MongoClient
from datetime import datetime
import random
import time
import google.auth
from google.auth.transport.requests import AuthorizedSession
from vertexai.tuning import sft
from vertexai.generative_models import GenerativeModel
import re

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"
socketio = SocketIO(app)

# Setup for Vertex API calls
credentials, _ = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)
google_session = AuthorizedSession(credentials)

# Initialize the bots
tuning_job_name = f"projects/frozone-475719/locations/us-central1/tuningJobs/3296615187565510656"
# For right now, all three point to the same tuning job
hottj = sft.SupervisedTuningJob(tuning_job_name)
cooltj = sft.SupervisedTuningJob(tuning_job_name)
frotj = sft.SupervisedTuningJob(tuning_job_name)
# Create the bot models
hotbot = GenerativeModel(hottj.tuned_model_endpoint_name)
coolbot = GenerativeModel(cooltj.tuned_model_endpoint_name)
frobot = GenerativeModel(frotj.tuned_model_endpoint_name)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["chatApp_test"]
rooms_collection = db.rooms

# List of fruits to choose display names from
FRUIT_NAMES = ["apple", "banana", "blueberry", "strawberry", "orange", "grape", "cherry"]
aliases = {"watermelon":"W", "apple":"A", "banana":"B", "blueberry":"C", "strawberry":"D", "orange":"E", "grape":"G", "cherry":"H"}
reverse_aliases = { value:key for key,value in aliases.items() }
# List of discussion topics
TOPICS_LIST = [
    {
        "title": "Abortion",
        "text": "Since the Supreme Court overturned Roe vs. Wade in 2022, there has been an increase in patients crossing state lines to receive abortions in less restrictive states. Pro-choice advocates argue that these restrictions exacerbate unequal access to healthcare due to financial strain and other factors and believe that a patient should be able to make personal medical decisions about their own body and future. Pro-life advocates argue that abortion legislation should be left to the states and believe that abortion is amoral and tantamount to murder. Both sides disagree on how to handle cases of rape, incest, terminal medical conditions, and risks to the mother’s life and health. What stance do you take on abortion and why?",
        "post": "Idk its hard bc both sides have good points. People should be able to make their own decisions about their own body but theres also moral stuff to think about too you know"
    },
    {
        "title": "Gun Rights/Control",
        "text": "Gun rights advocates argue that the right to bear arms is a protected second amendment right necessary for self-defense. Meanwhile, gun control advocates argue that stricter regulations are necessary to reduce gun violence. Potential reforms include stricter background checks, banning assault weapons, enacting red flag laws, and increasing the minimum age to purchase a gun. What stance do you take on gun rights vs. gun control and why?",
        "post": "i think people should be able to own guns but there has to be some check like background stuff so crazy people dont get them"
    },
    {
        "title": "Education and Trans Students",
        "text": "Laws and policies affecting trans people are highly contested, especially those involving education. Several states have passed laws restricting the use of preferred pronouns and names in schools, limiting transgender athletes' ability to participate in sports, and banning books containing LGBTQ+ content from school libraries. How do you think decisions on school policies regarding trans students should be made and why?",
        "post": "I dont think its that big a deal to use different pronouns but also trans athletes should be playing with the gender they were born as. I know thats an unpopular opinion but its the only way its fair."
    },
    {
        "title": "Immigration and ICE Activity",
        "text": "The current year has seen an increase in ICE (U.S. Immigration and Customs Enforcement) activity, including raids at workplaces, courthouses, schools, churches, and hospitals. Some argue that ICE is going too far and is violating the Constitutional due process rights of both immigrants and citizens. Others argue that these actions are necessary to maintain national security and enforce immigration law. What stance do you take on recent ICE activity and why?",
        "post": "I think ice is doing their job they're literally immigration enforcement. It sucks but if you come here illegally youre going to face the consequence."
    },
    {
        "title": "Universal Healthcare",
        "text": "Some argue that universal healthcare is necessary to ensure everyone has access to lifesaving medical treatments and a minimum standard of living, regardless of income or employment. Others argue that the choice of how to access healthcare is a private responsibility and that it is more efficient for the government to limit intervention. What stance do you take on government involvement in providing healthcare and why?",
        "post": "I think people should handle their own healthcare. the government is slow plus competition means more innovation. i dont trust the idea of one size fits all"
    }
] 

# Randomly select fruits to use for display names
def choose_names(n):
    # Return n unique random fruit names
    return random.sample(FRUIT_NAMES, n)

# Send initial watermelon post
def send_initial_post(room_id, delay):
    # Wait 1 second before sending
    time.sleep(delay)
    # Get the inital post for this topic
    room_doc = rooms_collection.find_one({"_id": room_id})
    topic_title = room_doc["topic"]
    topic_info = next((t for t in TOPICS_LIST if t["title"] == topic_title), None)
    if not topic_info:
        return
    initialPost = topic_info["post"]
    # Store the initial post in the database
    db_msg = {
        "sender": "watermelon",
        "message": initialPost,
        "timestamp": datetime.utcnow()
    }
    rooms_collection.update_one(
        {"_id": room_id},
        {"$push": {"messages": db_msg}}
    )
    # Send to the client (must use emit when in background thread)
    socketio.emit("message", {"sender": "watermelon", "message": initialPost}, to=room_id)

# Send message that a bot joined the room
def send_bot_joined(room_id, bot_name, delay):
    # Wait 1 second before sending
    time.sleep(delay)
    socketio.emit("message", {"sender": "", "message": f"{bot_name} has entered the chat"}, to=room_id)

# Ask a bot for its response, store in DB, and send to client
def ask_bot(room_id, bot, bot_display_name):
    # Prevents crashing if bot model did not load
    if bot is None:
        return
    # Get the full chat room history
    room_doc = rooms_collection.find_one({"_id": room_id})
    history = room_doc["messages"]
    # Build the LLM prompt
    prompt = ""
    for message in history:
        prompt += f"{aliases[message['sender']]}: {message['message']}\n"

    print("\n\n\n")
    print(prompt)
    print("\n\n\n")


    # Get the bot's response
    response = bot.generate_content(prompt)
    parsed_response = response.candidates[0].content.parts[0].text.strip()
    #sub letters for names, so if the bot addressed A -> Apple
    named_response = str(parsed_response)
    for letter in set(re.findall(r"\b[A-Z]\b", named_response)):
        if letter in reverse_aliases:
            named_response = re.sub(r"\b" + letter + r"\b", reverse_aliases[letter], named_response)

    # TODO: Add latency/wait time and staggering of bot responses 

    # Store the response in the database
    bot_message = {
        "sender": bot_display_name,
        "message": parsed_response,
        "timestamp": datetime.utcnow()
    }
    rooms_collection.update_one(
        {"_id": room_id},
        {"$push": {"messages": bot_message}}
    )
    
    # Check for if the bot passed (i.e. response = "(pass)")
    if (parsed_response == "(pass)"):
        return  # a pass is still recorded in the database, but not sent to the client

    # Send the bot's response to the client
    send({"sender": bot_display_name, "message": named_response}, to=room_id)


# Build the routes
@app.route('/', methods=["GET"])
def landing():
    return render_template('landing.html')
@app.route('/wait', methods=["GET"])
def waiting():
    return render_template('waiting.html')

@app.route('/chat', methods=["GET", "POST"])
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
    topic_info = next((t for t in TOPICS_LIST if t["title"] == topic), None)
    if topic_info is None:
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
        "topic": topic_info['title'],
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
    topic = room_doc["topic"]
    topic_info = next((t for t in TOPICS_LIST if t["title"] == topic), None)
    if topic_info is None:
        return redirect(url_for('topics'))
    return render_template("room.html", room=room_id, topic_info=topic_info, user=display_name, messages=room_doc["messages"], FroBot_name=room_doc["FroBot_name"], HotBot_name=room_doc["HotBot_name"], CoolBot_name=room_doc["CoolBot_name"])

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
    room_doc = rooms_collection.find_one({"_id": room})
    if not room_doc:
        return
    join_room(room)
    # Send the message that "watermelon" has already joined the chat
    send({
        "sender": "",
        "message": "watermelon has entered the chat"
    }, to=room)
    # Send the message that this user has joined the chat
    send({
        "sender": "",
        "message": f"{name} has entered the chat"
    }, to=room)
    # Start background task for CoolBot to join after a short delay
    socketio.start_background_task(send_bot_joined, room, room_doc['CoolBot_name'], 3)
    # Start background task to send the initial watermelon post after a short delay
    socketio.start_background_task(send_initial_post, room, 5)
    # Start background task for FroBot & HotBot to join after a short delay
    socketio.start_background_task(send_bot_joined, room, room_doc['FroBot_name'], 9)
    socketio.start_background_task(send_bot_joined, room, room_doc['HotBot_name'], 13)

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
    # Store the full version in the database
    rooms_collection.update_one(
        {"_id": room},
        {"$push": {"messages": db_message}}
    )
    # Send only the client version (no datetime)
    send(client_message, to=room)

    # Get the bot's display names
    room_doc = rooms_collection.find_one({"_id": room})
    frobot_name = room_doc["FroBot_name"]
    hotbot_name = room_doc["HotBot_name"]
    coolbot_name = room_doc["CoolBot_name"]
    # Ask each bot for a response
    ask_bot(room, frobot, frobot_name)
    ask_bot(room, hotbot, hotbot_name)
    ask_bot(room, coolbot, coolbot_name)

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

