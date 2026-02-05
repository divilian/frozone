#!/usr/bin/env python3
"""
weird_char_remover.py - This module provides `remove_weird_characters(text,
...)`, which replaces various malformed characters (often from Reddit) with
substitutes.
"""
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Remove weird characters (like from Reddit).")
    return parser.parse_args()


def remove_weird_characters(
    text: str,
) -> str:

    text = text.replace("&gt; ","> ")
    text = text.replace("&gt;","> ")
    return text


if __name__ == "__main__":

    args = parse_args()

    s = input("Enter text: ")
    while s != "done":
        deweirded = remove_weird_characters(s)
        print(f"De-weirded version: {deweirded}")
        s = input("Enter text: ")
