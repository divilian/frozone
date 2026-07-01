#!/usr/bin/env python3

import argparse
import textwrap
from datetime import datetime, timedelta
from pymongo import MongoClient


DB_NAME = "huggingFaceData"
COLLECTION_NAME = "rooms"
OFFSET = timedelta(hours=17)   # Frozone's clock is 17 hours ahead


def normalize_user_ids(raw_args):
    result = []

    for raw_arg in raw_args:
        for piece in raw_arg.split(","):
            user_id = piece.strip()

            if not user_id:
                continue

            if len(user_id) >= 2:
                if (
                    user_id[0] == user_id[-1]
                    and user_id[0] in {"'", '"'}
                ):
                    user_id = user_id[1:-1].strip()

            if user_id:
                result.append(user_id)

    return result


def replace_everywhere(obj, mapping):
    """
    Recursively walks a nested JSON-like structure and:
      • replaces substrings inside string VALUES
      • renames DICT KEYS if the key contains a mapping key as a substring

    mapping: dict {string_to_find: replacement_string}
    """

    if isinstance(obj, str):
        new = obj
        for k, v in mapping.items():
            new = new.replace(k, v)
        return new

    if isinstance(obj, list):
        return [replace_everywhere(item, mapping) for item in obj]

    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            new_key = key
            for k, v in mapping.items():
                new_key = new_key.replace(k, v)

            new_value = replace_everywhere(value, mapping)
            new_dict[new_key] = new_value

        return new_dict

    return obj


def parse_mongo_date(value):
    """
    Accepts either:
      - {'$date': '2025-11-24T21:14:04.499Z'}
      - a Python datetime object (as returned by pymongo)
    Returns a datetime.
    """
    if isinstance(value, datetime):
        return value

    if isinstance(value, dict) and "$date" in value:
        iso_str = value["$date"].replace("Z", "+00:00")
        return datetime.fromisoformat(iso_str)

    raise TypeError(f"Unsupported date format: {value!r}")


def parse_dates(created_at, last_activity):
    """
    created_at, last_activity: MongoDB datetime values
    Returns:
      (date_str, minutes_diff_rounded)
    """
    created_dt = parse_mongo_date(created_at) - OFFSET
    last_dt = parse_mongo_date(last_activity) - OFFSET

    date_str = created_dt.strftime("%A") + " " + created_dt.date().isoformat()
    diff_seconds = (last_dt - created_dt).total_seconds()
    minutes = round(diff_seconds / 60)

    return date_str, int(minutes)


def pretty_print(room):
    print("===============================================================")
    print(f"Mongo ID: {room['_id']}, room ID: {room['user_id']}")
    date, mins = parse_dates(room["created_at"], room["last_activity"])
    print(f"Date: {date}")
    print(f"Total: {mins} minutes")

    if room.get("aborted"):
        print("ABORTED")
    if not room.get("ended", False):
        print("NOT ended")

    print()
    print("----------------------------------")

    for msg in room.get("messages", []):
        sender = msg.get("sender", "")
        message = msg.get("message", "")
        for line in textwrap.wrap(f"{sender}: {message}", width=140):
            print(line)
        print("----------------------------------")

    print("\f")  # pagebreak


def print_missing_user_id(user_id):
    print("*******************")
    print(f"*** missing user_id {user_id} ***")
    print("*******************")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and pretty print Frozone chats from MongoDB."
    )
    parser.add_argument(
        "user_ids",
        nargs="+",
        help=(
            "One or more user IDs. May be space-separated or comma-separated; "
            "individual IDs may also be wrapped in single or double quotes."
        ),
    )
    parser.add_argument(
        "--uri",
        default="mongodb://localhost:27017",
        help="MongoDB connection URI (default: mongodb://localhost:27017)",
    )

    args = parser.parse_args()

    normalized_user_ids = normalize_user_ids(args.user_ids)
    if not normalized_user_ids:
        raise ValueError("No usable user_ids were provided.")

    client = MongoClient(args.uri)
    collection = client[DB_NAME][COLLECTION_NAME]

    for user_id in normalized_user_ids:
        room = collection.find_one({"user_id": user_id})

        if room is None:
            print_missing_user_id(user_id)
            continue

        name_map = {
            "watermelon": "OP",
            room["CoolBot_name"]: "CoolBot",
            room["FroBot_name"]: "FroBot",
            room["HotBot_name"]: "HotBot",
            room["user_name"]: "User",
        }

        room["messages"] = replace_everywhere(room.get("messages", []), name_map)
        pretty_print(room)


if __name__ == "__main__":
    main()