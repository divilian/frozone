import csv
import json
from pathlib import Path
from typing import List, Union

def csvs_to_jsonl(
    csv_files: Union[str, List[str]],
    output_path: str,
    system_instructions: str = "INSTRUCTIONS"
):
    """
    Convert one or more CSV files with columns:
    user_message, ai_response, dialogue_id, response_id, episode_done, issue_labels
    into a single JSONL file of the form:
    {
        "systemInstruction": {"role": "system", "parts": [{"text": "..."}]},
        "contents": [ ... ]
    }
    """

    if isinstance(csv_files, str):
        csv_files = [csv_files]

    all_rows = []

    # Read all CSVs
    for file in csv_files:
        print(file)
        with open(file, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Normalize types
                row["dialogue_id"] = int(row["dialogue_id"])
                row["response_id"] = int(row["response_id"])
                row["episode_done"] = str(row["episode_done"]).strip().lower() == "true"
                all_rows.append(row)

    # Sort to ensure order
    all_rows.sort(key=lambda r: (r["dialogue_id"], r["response_id"]))

    # Group into episodes
    episodes = []
    current_dialogue_id = None
    current_contents = []

    for row in all_rows:
        # Start new dialogue if needed
        if current_dialogue_id is None:
            current_dialogue_id = row["dialogue_id"]

        # Add user + model turns
        print(row)
        user_msg = row["user_message"].strip()
        ai_resp = row["ai_response"].strip()

        current_contents.append({"role": "user", "parts": [{"text": user_msg}]})
        current_contents.append({"role": "model", "parts": [{"text": ai_resp}]})

        # If this episode is done, finalize
        if row["episode_done"]:
            episodes.append({
                "systemInstruction": {
                    "role": "system",
                    "parts": [{"text": system_instructions}]
                },
                "contents": current_contents
            })
            current_contents = []
            current_dialogue_id = None

    # Write to JSONL
    output_path = Path(output_path)
    with output_path.open("w", encoding="utf-8") as out_f:
        for ep in episodes:
            json.dump(ep, out_f, ensure_ascii=False)
            out_f.write("\n")

    print(f"Wrote {len(episodes)} episodes to {output_path}")

# Use the function here:
csvs_to_jsonl(
    csv_files=[
        "data/frobot_training/bias.csv",
        "data/frobot_training/misinformation.csv",
        "data/frobot_training/misrepresentation.csv",
        "data/frobot_training/pass.csv",
        "data/frobot_training/prodding.csv",
        "data/frobot_training/toxicity.csv",
    ],
    output_path="data/frobot_training/merged_training_data.jsonl",
    system_instructions="N/A for now"
)

# run python -m data.training_data_to_jsonl