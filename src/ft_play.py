#!/usr/bin/env python3
# Interactively play with a fine-tuned Vertex AI model, giving it back the
# accumulated prompt as necessary so it's not stateless.
import os
import requests
import time
import random
import sys
import argparse
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

import vertexai
from vertexai.tuning import sft
from vertexai.generative_models import GenerativeModel
from google.cloud import aiplatform_v1
import google.auth
from google.auth.transport.requests import AuthorizedSession

from auth_setup import PROJECT_ID, REGION, ZONE, ensure_gcloud
ensure_gcloud()

BOT_NAME = "hotbot"   # Frobot/Hotbot/Coolbot/etc

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Play with fine-tuned model.")
    parser.add_argument(
        "tuning_job_id",
        type=int,
        help="The tuning job ID, which can be obtained from running
'showtuningjobs succeeded' and reading carefully. Pirates can always be reached
at 117775339060461568."
    )
    args = parser.parse_args()

    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    session = AuthorizedSession(credentials)

    tuning_job_name = f"projects/{PROJECT_ID}/locations/{REGION}/tuningJobs/{args.tuning_job_id}"

    uri = f"https://{REGION}-aiplatform.googleapis.com/v1/{tuning_job_name}"
    resp = session.get(uri)
    resp.raise_for_status()
    data = resp.json()
    display_name = data.get("tunedModelDisplayName")

    tj = sft.SupervisedTuningJob(tuning_job_name)
    tm = GenerativeModel(tj.tuned_model_endpoint_name)

    accumulated_content = ""

    new_input = input(f"Type something to {display_name}> ")
    while new_input != "done":
        accumulated_content += new_input
        response = tm.generate_content(accumulated_content)
        response_txt = response.candidates[0].content.parts[0].text
        print(f"Response was: {response_txt}")
        accumulated_content += response_txt
        new_input = input(f"Type something to {display_name}> ")
