import os
import requests
import time
import random

# In your environment (.bashrc, e.g.) do: export GEMINI_API_KEY=your_key
API_KEY = os.getenv("GEMINI_API_KEY")
# Note: we probably want "pro" instead of "flash" below. Using flash for now
# since it has lower latency.  - SD
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


def post_w_backoff(url, *, headers=None, json=None, timeout=60, tries=6):
    for i in range(tries):
        try:
            r = requests.post(url, headers=headers, json=json, timeout=timeout)
            if r.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(response=r)
            r.raise_for_status()
            return r
        except (requests.RequestException) as e:
            if i == tries - 1:
                raise
            time.sleep(random.uniform(0, 2 ** i))

def append_to_payload(payload, text, role="user"):
    payload['contents'].append(
        {
            "role": role,
            "parts": [
                { 'text': text }
            ] 
        }
    )

payload = {
    "contents": [
        {
            "role": "user",
            "parts": [
                {"text": "Placeholder"}
            ]
        }
    ]
}

headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": API_KEY,
}

new_input = input("> ")
payload['contents'][0]['parts'][0]['text'] = new_input
while new_input != "done":
    resp = post_w_backoff(URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    response = resp.json()['candidates'][0]['content']['parts'][0]['text']
    print(f"Response was: {response}")
    append_to_payload(payload, response, "model")
    new_input = input("\n> ")
    append_to_payload(payload, new_input, "user")
