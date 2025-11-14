#!/usr/bin/env python3
# Do everything freaking necessary to get all Vertex-AI-related logins properly
# connected and refreshed, all IPython-crash-related garbage worked around, and
# in general produce a happy world.
import vertexai
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ID = "frozone-475719"
REGION = "us-central1"
LOCATION = "us-central1"
ZONE = "us-central1-c"

vertexai.init(project=PROJECT_ID, location=LOCATION)

def run_quiet(cmd):
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return result.returncode == 0
    except FileNotFoundError:
        print(f"Command not found: {' '.join(cmd)}", file=sys.stderr)
        return False


def ensure_gcloud_user_auth():
    if not run_quiet(["gcloud", "auth", "print-access-token"]):
        print("No gcloud user auth found. Launching browser login...")
        subprocess.check_call(["gcloud", "auth", "login"])


def ensure_adc():
    if run_quiet(["gcloud", "auth", "application-default", "print-access-token"]):
        return

    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
    if creds_path and Path(creds_path).is_file():
        print(
            f"ADC via GOOGLE_APPLICATION_CREDENTIALS is set to: {creds_path}"
        )
        return

    print(
        "No ADC found. "
        "Launching browser login for Application Default Credentials..."
    )
    subprocess.check_call(["gcloud", "auth", "application-default", "login"])


# This is the main function to call from other scripts to make sure auth + ADC
# are set up.
def ensure_gcloud():
    try:
        ensure_gcloud_user_auth()
        ensure_adc()
        print("(Python: gcloud user auth and ADC are ready.)")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)

# <UGGH I HATE LIFE>
import IPython.display as _ipd
import IPython.core.display as _ipcd
if not hasattr(_ipcd, "display"):
    _ipcd.display = _ipd.display
# </UGGH I HATE LIFE>

ensure_gcloud()

