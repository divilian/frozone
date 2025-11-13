#!/usr/bin/env python3
# Interactively play with a fine-tuned Vertex AI model, giving it back the
# accumulated prompt as necessary so it's not stateless.
import os
import requests
import time
import random

import vertexai
from vertexai.tuning import sft
from vertexai.generative_models import GenerativeModel

from auth_setup import PROJECT_ID, REGION, ZONE, ensure_gcloud
ensure_gcloud()

TUNING_JOB_ID = 117775339060461568   # The pirate-tuned job

tj = sft.SupervisedTuningJob(f"projects/{PROJECT_ID}/locations/{REGION}/tuningJobs/{TUNING_JOB_ID}")
tm = GenerativeModel(tj.tuned_model_endpoint_name)

accumulated_content = ""

new_input = input("Type something> ")
while new_input != "done":
    accumulated_content += new_input
    response = tm.generate_content(accumulated_content)
    response_txt = response.candidates[0].content.parts[0].text
    print(f"Response was: {response_txt}")
    accumulated_content += response_txt
    new_input = input("\nType something> ")
