#!/usr/bin/env python3

import argparse
from pymongo import MongoClient


DB_NAME = "huggingFaceData"
COLLECTION_NAME = "rooms"
SEPARATOR = "=" * 79
MISSING_BORDER = "*" * 19


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


def build_sender_map(doc):
    return {
        "watermelon": "starter",
        doc["user_name"]: "user",
        doc["FroBot_name"]: "FroBot",
        doc["HotBot_name"]: "HotBot",
        doc["CoolBot_name"]: "CoolBot",
    }


def print_missing_user_id(user_id):
    print(MISSING_BORDER)
    print(f"*** missing user_id {user_id} ***")
    print(MISSING_BORDER)


def print_room(doc):
    sender_map = build_sender_map(doc)

    print(SEPARATOR)
    print(f"user_id: {doc['user_id']}")
    print(f"topic: {doc['topic']}")

    for msg in doc.get("messages", []):
        sender = msg.get("sender", "")
        message_text = msg.get("message", "")
        display_name = sender_map.get(sender, sender)
        print(f"{display_name}: {message_text}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Fetch room documents by user_id from MongoDB and print them "
            "in a simplified transcript format."
        )
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
        doc = collection.find_one({"user_id": user_id})

        if doc is None:
            print_missing_user_id(user_id)
        else:
            print_room(doc)


if __name__ == "__main__":
    main()
