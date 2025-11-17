from flask import Flask, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, send
from pymongo import MongoClient
from datetime import datetime
import random
import vertexai
from vertexai.tuning import sft
from vertexai.generative_models import GenerativeModel

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"
socketio = SocketIO(app)

"""
# Initialize FroBot, HotBot, and CoolBot Models
vertexai.init(
    project="frozone-475719",
    location="us-central1"
)
# For right now, all three point to the same tuning job
TUNING_JOB_ID = "117775339060461568" # the pirate model ID
hottj = sft.SupervisedTuningJob(f"projects/frozone-475719/locations/us-central1/tuningJobs/{TUNING_JOB_ID}")
cooltj = sft.SupervisedTuningJob(f"projects/frozone-475719/locations/us-central1/tuningJobs/{TUNING_JOB_ID}")
frotj = sft.SupervisedTuningJob(f"projects/frozone-475719/locations/us-central1/tuningJobs/{TUNING_JOB_ID}")
# Create the bot models
hotbot = GenerativeModel(hottj.tuned_model_endpoint_name)
coolbot = GenerativeModel(cooltj.tuned_model_endpoint_name)
frobot = GenerativeModel(frotj.tuned_model_endpoint_name)
"""

client = MongoClient("mongodb://localhost:27017/")
db = client["chatApp_test"]
rooms_collection = db.rooms

FRUIT_NAMES = ["apple", "banana", "blueberry", "strawberry", "orange", "grape", "cherry"]
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

def choose_names(n):
    # Return n unique random fruit names
    return random.sample(FRUIT_NAMES, n)

"""
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
        prompt += f"{message['sender']}: {message['message']}\n"
    # Get the bot's response
    response = bot.generate_content(prompt)
    parsed_response = response.candidates[0].content.parts[0].text.strip()
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
    # Send the bot's response to the client
    send({"sender": bot_display_name, "message": parsed_response}, to=room_id)
"""

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
    # Store the full version in the database
    rooms_collection.update_one(
        {"_id": room},
        {"$push": {"messages": db_message}}
    )
    # Send only the client version (no datetime)
    send(client_message, to=room)

    """
    # Get the bot's display names
    room_doc = rooms_collection.find_one({"_id": room})
    frobot_name = room_doc["FroBot_name"]
    hotbot_name = room_doc["HotBot_name"]
    coolbot_name = room_doc["CoolBot_name"]
    # Ask each bot for a response
    ask_bot(room, frobot, frobot_name)
    ask_bot(room, hotbot, hotbot_name)
    ask_bot(room, coolbot, coolbot_name)
    """

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

