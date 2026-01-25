#!/usr/bin/env python3
"""
corrupter.py - light English typo/misspelling injection for to simulate
"human-typed" text.

This module provides `corrupt(text, ...)`, which returns the original text with
a small amount of realistic noise (common misspellings and keyboard typos). See
function docstring for arguments and explanations.
"""
import re
import argparse
import random

import nlpaug.augmenter.word as naw
import nlpaug.augmenter.char as nac
from nlpaug.flow import Sequential


def parse_args():
    parser = argparse.ArgumentParser(
        description="Interactive text corrupter.")
    parser.add_argument(
        "--misspelling-prob",
        type=float,
        default=0.04,
        help="Fraction of words to misspell (roughly)"
    )
    parser.add_argument(
        "--typo-prob",
        type=float,
        default=0.01,
        help="Fraction of words to finger fart"
    )
    parser.add_argument(
        "--min-len",
        type=int,
        default=3,
        help="Minimum length word to possibly corrupt"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="If True, print words and corruptions (if any)."
    )
    return parser.parse_args()


def corrupt(
    text: str,
    misspell_prob: float,
    typo_prob: float,
    min_len: int,
    misspell_aug_p: float = 0.02,
    typo_aug_p: float = 0.001,
    verbose: bool = False
) -> str:
    """
    Modestly corrupt the text passed to get a version with a small number of
    misspellings and typos.

    misspell_prob: Probability of each word (of sufficient length) being
        misspelled.
    typo_prob: Probability of each word (of sufficient length) having a typo.
    min_len: The minimum length word that will be considered for corruption.
    misspell_aug_p: Passed through directly to the nlpaug.augmenter. From their
        docs, it seems to mean "for words chosen for misspelling, what
        percentage of the word is misspelled?"
    typo_aug_p: Passed through directly to the nlpaug.augmenter. From their
        docs, it seems to mean "for words chosen for typos, what percentage of
        the word will have typos?"
    verbose: if True, print words as encountered, plus their corruptions (if
        any).
    """

    TOKEN_RE = re.compile(
        r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?|\s+|[^\w\s]",
        re.UNICODE
    )
    WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z0-9]+)?", re.UNICODE)

    misspell_aug = naw.SpellingAug(aug_p=misspell_aug_p)
    typo_aug = nac.KeyboardAug(aug_word_p=typo_aug_p)

    tokens = TOKEN_RE.findall(text)
    for i in range(len(tokens)):
        if verbose: print(f"Considering {tokens[i]}...")
        if WORD_RE.fullmatch(tokens[i]):
            if len(tokens[i]) >= min_len and random.random() < misspell_prob:
                tokens[i] = misspell_aug.augment(tokens[i])[0]
                if verbose: print(f"  ...misspelled to {tokens[i]}")
            if len(tokens[i]) >= min_len and random.random() < typo_prob:
                tokens[i] = typo_aug.augment(tokens[i])[0]
                if verbose: print(f"  ...corrupted to {tokens[i]}")

    return "".join(tokens)


if __name__ == "__main__":

    random.seed(123)

    args = parse_args()

    s = input("Enter text: ")
    while s != "done":
        corrupted = corrupt(
            s,
            args.misspelling_prob,
            args.typo_prob,
            args.min_len,
            verbose=args.verbose,
        )
        print(f"Corrupted version: {corrupted}")
        s = input("Enter text: ")
