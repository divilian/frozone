#!/usr/bin/env python3
"""
quote_remover.py - eliminate entire posts being quoted.

This module provides `remove_quotes(text, ...)`, which removes any extraneous
outer quotes.
"""
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Interactive quote remover.")
    return parser.parse_args()


def remove_quotes(
    text: str,
) -> str:

    if (
        (text.startswith('"') or text.startswith("'")) and
        (text.endswith('"') or text.endswith("'"))
    ):
        return text[1:-1]
    return text


if __name__ == "__main__":

    args = parse_args()

    s = input("Enter text: ")
    while s != "done":
        removed = remove_quotes(s)
        print(f"Removed version: {removed}")
        s = input("Enter text: ")
