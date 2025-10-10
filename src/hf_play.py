# Project Frozone
# (C) 2025

import sys
import argparse

import torch
from transformers import (
    AutoConfig,
    AutoModelForSequenceClassification,
    AutoTokenizer
)

torch.set_printoptions(precision=4, sci_mode=False)


def load_model(model_name: str):
    print(f"Loading model {model_name}...")
    cfg = AutoConfig.from_pretrained(model_name)
    tok = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device).eval()
    return cfg, tok, model, device


if __name__ == "__main__":

    parser = argparse.ArgumentParser("HF interactive playground")
    parser.add_argument(
        "model",
        nargs="?",
        help="full HF model name",
        default="minh21/XLNet-Reddit-Toxic-Comment-Classification"
    )

    args = parser.parse_args()

    with torch.inference_mode():

        cfg, tok, model, device = load_model(args.model)

        # If no PAD token, reuse EOS (or UNK) as PAD
        if tok.pad_token is None:
            tok.pad_token = tok.eos_token or tok.unk_token
            model.config.pad_token_id = tok.pad_token_id

        text = input("Enter text (or 'done'): ")
        while text != "done":

            encoded = tok(
                text,
                padding=True,
                truncation=True,
                max_length=256,
                return_tensors="pt",
            )
            encoded = {k: v.to(device) for k, v in encoded.items()}
            out = model(**encoded)
            logits = out.logits.squeeze()

            # Multi-label classification: there are multiple, non-exclusive
            #   categories, and the text will get a separate, independent
            #   score for each. Example: a classifier that measures beauty on a
            #   0-to-1 scale, toxicity on a 0-to-1 scale, and interestingness
            #   on a 0-to-1 scale. We want to use *sigmoid* to convert logits
            #   to probabilities.
            # Single-label classification: there are mutually exclusive
            #   categories, and the text will get a relative score for each,
            #   indicating how probable each label is. Example: a classifier
            #   that determines whether a text is on politics, sports, or
            #   entertainment, and how likely each of these mutually exclusive
            #   labels is to the correct answer. We want to use *softmax* to
            #   convert logits to probabilities.
            if cfg.problem_type == "multi_label_classification":
                probs = torch.sigmoid(logits)
            elif cfg.problem_type == "single_label_classification":
                probs = torch.softmax(logits, dim=-1)
            else:
                print("Gah -- problem type not set! Lazy modeler...")
                if cfg.num_labels == 1:
                    print("Assuming multi-label...")
                    probs = torch.sigmoid(logits)
                else:
                    print("Assuming single-label...")
                    probs = torch.softmax(logits, dim=-1)

            probs = probs.detach().cpu().tolist()
            for labelnum in range(len(cfg.id2label)):
                print(f"{cfg.id2label[labelnum]:>14}: {probs[labelnum]:.4f}")

            text = input("Enter text (or 'done'): ")
