import bson, json
import os
import textwrap
from datetime import datetime
import argparse

#change this to the bson chatlog file you want to look at.  Or provide an input command line argument (see below)
DEFAULT_FILE = "data/experiment_results/Frozone_Data/chatlogs/chatrooms_4-14.bson"

parser = argparse.ArgumentParser()
parser.add_argument(
    #the path to the BSON source file for the chatlog
    "input",
    nargs="?",
    default=DEFAULT_FILE,
    help="Input BSON file"
)
parser.add_argument(
    #the output directory where files will be saved
    "-o",
    "--output",
    default="./",
    help="Output directory location"
)
parser.add_argument(
    #optional list the ids in JSON ex --ids='["id1","id2"]'
    #if nothing specified, all ids in the BSON chatlogs will be output
    "--ids",
    type=json.loads,
    default=None,
    help="JSON of the user ids you want"
)

args = parser.parse_args()

# SETTINGS

USER_IDS = args.ids
# change this to whichever rooms you want

MAX_LINE_LENGTH = 80  # max line length; NONE for no line length

INPUT_FILE = args.input
OUTPUT_DIR = args.output

# SCRIPT

with open(INPUT_FILE, "rb") as f:
    data = bson.decode_all(f.read())

found_ids = set()

for doc in data:
    user_id = doc.get('user_id')
    if USER_IDS and user_id not in USER_IDS:
        continue

    found_ids.add(user_id)

    true_id_map = {}
    true_id_map[doc["user_name"]] = "User"
    true_id_map[doc["FroBot_name"]] = "Frobot"
    true_id_map[doc["CoolBot_name"]] = "Coolbot"
    true_id_map[doc["HotBot_name"]] = "Hotbot"
    true_id_map["watermelon"] = "Initiatorbot"

    lines = []
    lines.append(f"=== Room {doc['_id']} ===")
    lines.append(f"Topic: {doc.get('topic')}")
    lines.append(f"Created: {doc.get('created_at')}")
    lines.append(f"User: {doc.get('user_name')} ({doc.get('user_id')})")
    lines.append(f"Bots — Frobot: {doc.get('FroBot_name')}, Hotbot: {doc.get('HotBot_name')}, Coolbot: {doc.get('CoolBot_name')}")
    lines.append("\n--- Messages ---")
    for msg in doc.get('messages', []):
        ts = msg.get('timestamp', '')
        if isinstance(ts, datetime):
            ts = ts.strftime('%H:%M:%S')
        sender = msg.get('sender', '?')
        sender_true_id = true_id_map[sender]
        text = msg.get('message', '')
        line = f"  [{ts}] {sender} ({sender_true_id}): {text}"
        if MAX_LINE_LENGTH:
            prefix = " " * 4
            line = textwrap.fill(line, width=MAX_LINE_LENGTH, subsequent_indent=prefix)
        lines.append(line)

    filename = os.path.join(OUTPUT_DIR, f"chatlog_{doc['user_id']}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Saved {filename}")
if USER_IDS:
    for id in USER_IDS:
        if id not in found_ids:
            print(f"Room corresponding to user with ID {id} not found.")




