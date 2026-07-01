#!/usr/bin/env python
import json
import argparse
import textwrap
from datetime import datetime, timedelta

# Begin by exporting from Frozone MongoDB via:
# $ mongoexport \
#   --uri="mongodb://localhost:27017/experimentData" \
#   --collection=rooms \
#   --query='{"user_id": { "$regularExpression": { "pattern": "^[1-5][0-9]{3}", "options": "" }} }' \
#   --out=novDec2025.jsonl


def replace_everywhere(obj, mapping):
    """
    Recursively walks a nested JSON-like structure and:
      • replaces substrings inside string VALUES
      • renames DICT KEYS if the key contains a mapping key as a substring

    mapping: dict {string_to_find: replacement_string}
    """

    # If obj is a string, replace ALL substring matches
    if isinstance(obj, str):
        new = obj
        for k, v in mapping.items():
            new = new.replace(k, v)
        return new

    # If obj is a list → recurse on each item
    if isinstance(obj, list):
        return [replace_everywhere(item, mapping) for item in obj]

    # If obj is a dict → rename keys + recurse on values
    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():

            # 1. Rename the key by substring replacement
            new_key = key
            for k, v in mapping.items():
                new_key = new_key.replace(k, v)

            # 2. Recurse into the value
            new_value = replace_everywhere(value, mapping)

            new_dict[new_key] = new_value

        return new_dict

    # Otherwise (int, float, None, bool), leave unchanged
    return obj


def parse_mongo_date(date_dict):
    """
    date_dict: something like {'$date': '2025-11-24T21:14:04.499Z'}
    returns a timezone-aware datetime in UTC
    """
    iso_str = date_dict["$date"]
    # datetime.fromisoformat doesn't like 'Z', so convert to +00:00
    iso_str = iso_str.replace("Z", "+00:00")
    return datetime.fromisoformat(iso_str)


OFFSET = timedelta(hours=17)   # Frozone's clock is 17 hours ahead

def parse_dates(created_at, last_activity):
    """
    created_at, last_activity: dicts with a '$date' ISO string
    Returns:
      (date_str, minutes_diff_rounded)
    """
    created_dt = parse_mongo_date(created_at) - OFFSET
    last_dt = parse_mongo_date(last_activity) - OFFSET

    # (1) Pretty date string from created_at
    date_str = created_dt.strftime("%A") + " " + created_dt.date().isoformat()

    # (2) Rounded minutes difference
    diff_seconds = (last_dt - created_dt).total_seconds()
    minutes = round(diff_seconds / 60)

    return date_str, int(minutes)


def pretty_print(room):
    print("===============================================================")
    print(f"Mongo ID: {room['_id']}, room ID: {room['user_id']}")
    date, mins = parse_dates(room['created_at'],room['last_activity'])
    print(f"Date: {date}")
    print(f"Total: {mins} minutes")
    if room['aborted']:
        print("ABORTED")
    if not room['ended']:
        print("NOT ended")
    print()
    print("----------------------------------")
    for msg in room['messages']:
        for l in textwrap.wrap(f"{msg['sender']}: {msg['message']}", width=140):
            print(l)
        print("----------------------------------")
    print("\f")  # pagebreak


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Extract and pretty print Frozone chats from file.")
    parser.add_argument(
        "JSONLfile",
        type=str,
        help="a JSONL file that was dumped from Mongo (see comments)."
    )
    args = parser.parse_args()

    rooms = []
    with open(args.JSONLfile,"r",encoding="utf-8") as f:
        for line in f:
            room = json.loads(line)
            name_map = {
                'watermelon':'OP',
                room['CoolBot_name']:'CoolBot',
                room['FroBot_name']:'FroBot',
                room['HotBot_name']:'HotBot',
                room['user_name']:'User',
            }
            room['messages'] = replace_everywhere(room['messages'],name_map)
            rooms.append(room)

    for r in rooms:
        pretty_print(r)
