#!/usr/bin/env python
# Be sure to pip install google-cloud-storage.
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from auth_setup import PROJECT_ID, REGION, ZONE, ensure_gcloud
import makeIPythonSafe

import os
import argparse

import vertexai
from vertexai.tuning import sft
from google.cloud import storage

def ensure_bucket_exists(bucket_name: str, location: str):
    """Return a Bucket object, creating it if it does not exist."""
    client = storage.Client(project=PROJECT_ID)
    try:
        bucket = client.get_bucket(bucket_name)
    except Exception:
        # Bucket does not exist; create it
        bucket = client.bucket(bucket_name)
        bucket = client.create_bucket(bucket, location=location)
    return bucket


def upload_to_bucket(bucket, filename: str):
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Start fine-tuning job.")
    parser.add_argument(
        "display_name",
        type=str,
        help="A unique-ish name that will help you identify your freaking job from all the many others."
    )
    parser.add_argument(
        "train_dataset",
        type=str,
        help="The filename of the training dataset (in .jsonl format; see Noah's script to convert from .csv) in your local directory."
    )
    parser.add_argument(
        "--train_dataset_bucket",
        type=str,
        help=("""
            The name of the Google Cloud bucket you want to create (or which
            has already been created) to store your fine-tuning dataset. This
            must have only lowercase letters, numbers, dashes, and dots.
        """),
        default="frozone-tuning"
    )
    parser.add_argument(
        "--base_model",
        type=str,
        help="The name of the base model you want to use (default gemini-2.0-flash-001)",
        default="gemini-2.0-flash-001"
    )
    parser.add_argument(
        "--num_epochs",
        type=int,
        help="Number of epochs to tune (default 3).",
        default=3
    )
    args = parser.parse_args()

    # Normalize bucket name: strip optional gs:// prefix
    if args.train_dataset_bucket.startswith("gs://"):
        bucket_name = args.train_dataset_bucket[len("gs://") :]
    else:
        bucket_name = args.train_dataset_bucket
    bucket_name = "frozone-" + bucket_name

    # Ensure .jsonl extension
    if not args.train_dataset.endswith(".jsonl"):
        sys.exit("Training data set must end in .jsonl.")

    local_train_path = args.train_dataset
    if not os.path.isfile(local_train_path):
        sys.exit(f"Local training data file not found: {local_train_path}")

    # 1) Ensure bucket exists (create if missing)
    bucket = ensure_bucket_exists(bucket_name, REGION)

    # 2) Upload training file to bucket, overwriting if it already exists
    upload_to_bucket(bucket, args.train_dataset)

    sft_tuning_job = sft.train(
        source_model=args.base_model,
        train_dataset=f"gs://{bucket_name}/{args.train_dataset}",
        epochs=args.num_epochs,
        #learning_rate_multiplier=1,
        #adapter_size=4,
        tuned_model_display_name=args.display_name,

        # This ability may be useful to help identify some jobs from others. For
        # now, I just leave it with a silly value to show how it can be done.
        # (The rules about lowercase-letters-only-plus-dashes apply here.)
        labels={'i-can-make':'a-key-value-pair'}
    )

    # Full resource name, e.g.
    # projects/PROJECT_ID/locations/us-central1/tuningJobs/1234567890123456789
    job_resource_name = sft_tuning_job.resource_name

    # Just the numeric job ID (last path segment)
    job_id = job_resource_name.split("/")[-1]

    print(f"\nTuning job {job_id} ({args.display_name}) started!")
    print(f"Full resource name: {job_resource_name}")
    print(f"You can run showtuningjob {job_id} for updates.")
    print(f"You can run ft_play {job_id} once it's finished, to experiment.")
