from difflib import SequenceMatcher
import re

"""
Given a list of string messages (most reccent messages)
Check that (str) new_message is not an exact match of an 
existing message or very close in sequence.

Ex:
>>> recent_messages = ['this is a test']
>>> new_message = 'this is a test ok?'
>>> duplicate_check(new_message, recent_messages)
True
"""

#remove punctuation and extra whitespace
def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text

#checks for exact matches
def is_exact_duplicate(new_message, recent_messages):
    new_norm = normalize(new_message)
    return any(new_norm == normalize(m) for m in recent_messages)

#calculate sequence similarity
#https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher.ratio
def similarity(a, b):
    if len(a) < len(b):
        return SequenceMatcher(None, a, b).ratio()
    else:
        return SequenceMatcher(None, b, a).ratio()

#checks for duplicate messages with minor differences
def is_similar_duplicate(new_message, recent_messages, threshold=0.9):
    new_norm = normalize(new_message)
    for message in recent_messages:
        message_norm = normalize(message)
        if similarity(new_norm, message_norm) >= threshold:
            return True
    return False

#check everything
def duplicate_check(new_message, recent_messages, threshold=0.9):
    return is_exact_duplicate(new_message, recent_messages) or is_similar_duplicate(new_message, recent_messages, threshold)

