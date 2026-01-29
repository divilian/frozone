#!/usr/bin/env python3
"""
humanizer.py - remove bulleted lists, markdown bold indicators, titles, and
various other obviously-AI-written textual features, and replace them with more
human-like connective text.

This module provides `humanize(text, ...)`, which preserves the basic content
of the original text, but with a more human-like straight-prose expression. See
function docstring for arguments and explanations.
"""
import re
import random
import argparse
from typing import List


INTRO_PHRASES = [
    "On {topic}, ",
    "On the {topic} issue, ",
    "When it comes to {topic}, ",
    "As for {topic}, ",
    "Another thing is {topic}, ",  # yep, it's a comma splice! We're human.
    "People often claim that {topic}, but ",
    "People might say {topic}, but "
]

def strip_markdown(text: str) -> str:
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    return text

def is_bullet(line: str) -> bool:
    # Matches:
    #   * item
    #   - item
    #   • item
    #   1. item
    #   1) item
    return bool(
        re.match(r"^\s*(?:[*\-•]|(?:\d+[.)]))\s+", line)
    )

def extract_bullet_text(line: str) -> str:
    return re.sub(r"^\s*(?:[*\-•]|(?:\d+[.)]))\s+", "", line).strip()

def choose_intro(topic: str) -> str:
    phrase = random.choice(INTRO_PHRASES)
    return phrase.format(topic=topic.strip().lower())

def collapse_list(items: List[str]) -> str:
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + f", and {items[-1]}"

def lowercase_initial(text: str) -> str:
    """
    Lowercase the first alphabetic character in `text`.
    Leaves leading quotes/whitespace/punctuation intact.
    """
    chars = list(text)
    for i, ch in enumerate(chars):
        if ch.isalpha():
            chars[i] = ch.lower()
            break
    return "".join(chars)

def normalize_inline_bullets(text: str) -> str:
    """
    Turn inline bullet markers into real line-starting bullets.

    Example:
      "pay: * Sales taxes... * Property taxes..."
    becomes:
      "pay:\n* Sales taxes...\n* Property taxes..."
    """
    # Put a newline before any bullet marker that is preceded by whitespace,
    # but avoid changing bullets that are already at the start of a line.
    text = re.sub(r"(?m)(?<!^)\s+([*\-•])\s+", r"\n\1 ", text)

    # Also handle numbered bullets like " 1) foo" or " 1. foo"
    text = re.sub(r"(?m)(?<!^)\s+(\d+[.)])\s+", r"\n\1 ", text)

    return text

def humanize_chunk(text: str) -> str:

    text = normalize_inline_bullets(text)
    text = strip_markdown(text)
    lines = text.splitlines()

    output: List[str] = []

    current_sentence = None
    tail_items: List[str] = []

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            continue

        if is_bullet(line):
            item = extract_bullet_text(line)

            # Heading bullet: flush previous sentence first
            if ":" in item:
                if current_sentence:
                    if tail_items:
                        clean_items = [
                            lowercase_initial(ti.rstrip("."))
                            for ti in tail_items
                        ]
                        current_sentence += " " + collapse_list(clean_items)
                        tail_items = []

                    output.append(current_sentence)

                title, rest = item.split(":", 1)
                body = lowercase_initial(rest.strip())
                current_sentence = choose_intro(title) + body


            else:
                # Sub-bullet: belongs to current heading
                if current_sentence:
                    tail_items.append(item)
                else:
                    # orphan bullet (rare, but handle)
                    output.append(item)

        else:
            # Normal line flushes everything
            if current_sentence:
                if tail_items:
                    clean_items = [
                        lowercase_initial(ti.rstrip("."))
                        for ti in tail_items
                    ]
                    current_sentence += " " + collapse_list(clean_items)
                    tail_items = []

                output.append(current_sentence)
                current_sentence = None

            output.append(line)

    # Final flush
    if current_sentence:
        if tail_items:
            clean_items = [
                lowercase_initial(ti.rstrip("."))
                for ti in tail_items
            ]
            current_sentence += " " + collapse_list(clean_items)
        output.append(current_sentence)

    result = "\n\n".join(output)
    result = re.sub(r"[ \t]+", " ", result)
    return result

def humanize(text: str) -> str:
    paragraphs = re.split(r"\n\s*\n", text.strip())
    cleaned = [humanize_chunk(p) for p in paragraphs]
    return "\n\n".join(cleaned)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Interactive 'humanizer': replaces obviously AI-written "
        "content with more human-like comment.")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print verbose output for debugging."
    )
    return parser.parse_args()

if __name__ == "__main__":

    random.seed(123)

    args = parse_args()

    sample = """
* **Free Healthcare:** Undocumented immigrants generally do not receive free, comprehensive healthcare.
* **Other Benefits:** The vast majority of federally funded public benefits require legal status.
* **No Taxes:** This is a common misconception.
    * Sales taxes
    * Property taxes
    * Federal and state income taxes
"""
    print(f"\nSample humanized version:\n{humanize(sample)}")

    s = input("\nEnter text or filename (ending in .txt): ")
    while s and s != "done":
        if s.endswith(".txt"):
            with open(s, encoding='utf-8') as f:
                s = f.read()
        humanized = humanize(s)
        print(f"\nHumanized version: {humanized}")
        s = input("Enter text: ")
