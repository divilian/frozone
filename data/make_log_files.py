import bson
from datetime import datetime

USER_IDS = ['657fa05267050fd8b627f0bc', '662fb80a4da196677a2d2a16', '6644b750f83b1ad48d9ce14f', '6715b46f9f59f9e05837029a', '67e268cbf13dcd115337894c', '682a1996cd2cfa1f1160cb71', '683cbc0c0c2d722831c8bc17', '699397c4953cfe8ddd54a8f0', '69c2d2d68e61037f1e2f1a06', '69d7ebaa0c636510b15ce777']
  # change this to whichever rooms you want

with open("data/experiment_results/Frozone_Data/chatlogs/chatrooms_4-14.bson", "rb") as f:
    data = bson.decode_all(f.read())

found_ids = set()

for doc in data:
    user_id = doc.get('user_id')
    if user_id not in USER_IDS:
        continue

    # this is a relevant room
    found_ids.add(user_id)
    print(f"=== Room {doc['_id']} ===")
    print(f"Topic: {doc.get('topic')}")
    print(f"Created: {doc.get('created_at')}")
    print(f"User: {doc.get('user_name')} ({doc.get('user_id')})")
    print(f"Bots — Fro: {doc.get('FroBot_name')}, Hot: {doc.get('HotBot_name')}, Cool: {doc.get('CoolBot_name')}")
    print(f"\n--- Messages ---")
    for msg in doc.get('messages', []):
        ts = msg.get('timestamp', '')
        if isinstance(ts, datetime):
            ts = ts.strftime('%H:%M:%S')
        sender = msg.get('sender', '?')
        text = msg.get('message', '')
        print(f"  [{ts}] {sender}: {text}")

for id in USER_IDS:
    if id not in found_ids:
        print(f"Room corresponding to user with ID {id} not found.")