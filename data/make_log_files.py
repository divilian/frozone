import bson
import os
import textwrap
from datetime import datetime


# SETTINGS

USER_IDS = ['657fa05267050fd8b627f0bc', '662fb80a4da196677a2d2a16', '6644b750f83b1ad48d9ce14f', '6715b46f9f59f9e05837029a', '67e268cbf13dcd115337894c', '682a1996cd2cfa1f1160cb71', '683cbc0c0c2d722831c8bc17', '699397c4953cfe8ddd54a8f0', '69c2d2d68e61037f1e2f1a06', '69d7ebaa0c636510b15ce777']
  # change this to whichever rooms you want

MAX_LINE_LENGTH = 80  # max line length; NONE for no line length

OUTPUT_DIR = "data/experiment_results/Frozone_Data/chatlogs"


# SCRIPT

with open("data/experiment_results/Frozone_Data/chatlogs/chatrooms_4-14.bson", "rb") as f:
    data = bson.decode_all(f.read())

found_ids = set()

for doc in data:
    user_id = doc.get('user_id')
    if user_id not in USER_IDS:
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

for id in USER_IDS:
    if id not in found_ids:
        print(f"Room corresponding to user with ID {id} not found.")