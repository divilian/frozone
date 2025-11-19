#TO JSONL SINGLE COMMENT

import csv
import json
from pathlib import Path
from typing import List, Union
import sys

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
        "contents": 
            [
                {"role":"user","parts":["text":system_instructions,"text":user_input]},
                {"role":"model","parts":["text":ai_response]}
            ]
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
                row["episode_done"] = ((str(row["episode_done"]).strip().lower() == "true") or (str(row["episode_done"]) == "1"))
                all_rows.append(row)

    # Sort to ensure order
    all_rows.sort(key=lambda r: (r["dialogue_id"], r["response_id"]))

    # Group into episodes
    episodes = []
    current_dialogue_id = None
    cur_msg = ""
    current_contents = []
    toggle = True

    for row in all_rows:
        
        if current_dialogue_id is None:
            current_dialogue_id = row["dialogue_id"]

        print(row)
        user_msg = row["user_message"].strip()
        ai_resp = row["ai_response"].strip()

        if toggle:
            cur_msg = system_instructions + "\n" + user_msg
        else:
            cur_msg = cur_msg + "\n" + user_msg

        current_contents.append({"role": "user", "parts": [{"text":cur_msg}]})
        current_contents.append({"role": "model", "parts": [{"text":ai_resp}]})

        #adds the current sample 
        episodes.append({"contents":current_contents})
        current_contents = []

        #adds the response to the next sample if the next sample is not an episode done
        cur_mss = cur_msg + "\n<RE>: " + ai_resp

        #reset the full message at end of episode
        if row["episode_done"]:
            cur_msg = ""
            toggle = True
        else:
            toggle = False
            
    # Write to JSONL
    output_path = Path(output_path)
    with output_path.open("w", encoding="utf-8-sig") as out_f:
        for ep in episodes:
            json.dump(ep, out_f, ensure_ascii=False)
            out_f.write("\n")

    print(f"Wrote {len(episodes)} episodes to {output_path}")

# Use the function here:
if __name__ == "__main__":

    args = sys.argv

    if len(args) == 1:
        # frobot settings by default
        system_instructions = ""
        with open("../prompts/experiment/frobot_prompt.txt", "r", encoding="utf-8", errors="ignore") as f:
            system_instructions = f.read()
        csvs_to_jsonl(
            csv_files=[
                "./frobot_training/bias.csv",
                "./frobot_training/misinformation.csv",
                "./frobot_training/misrepresentation.csv",
                "./frobot_training/pass.csv",
                "./frobot_training/prodding.csv",
                "./frobot_training/toxicity.csv",
            ],
            output_path="./frobot_training/merged_training_data.jsonl",
            system_instructions=system_instructions
        )

    else:
        try:
            if len(args) != 3 and len(args) != 4:
                raise Exception("Usage: python training_data_to_jsonl.py f1.csv,f2.csv,f3.csv output.jsonl [-c|-f|-h|]")
            else:
                inputs = args[1].split(",")
                output = args[2]

                for f in inputs:
                    if ".csv" not in f:
                        raise Exception(f"File {f} is not a csv file!")
                    
                system_instructions="System instructions not provided"
                if len(args) == 4:
                    # populate system instructions
                    prompt_file = ""
                    if args[3] == '-c':
                        prompt_file = "../prompts/experiment/coolbot_prompt.txt"
                    elif args[3] == '-f':
                        prompt_file = "../prompts/experiment/frobot_prompt.txt"
                    elif args[3] == '-h':
                        prompt_file = "../prompts/experiment/hotbot_prompt.txt"
                    else:
                        raise Exception(f"Flag {args[3]} is invalid! Must be one of -c, -f, or -h.")

                    with open(prompt_file, "r", encoding="utf-8", errors="ignore") as f:
                        system_instructions = f.read()
                
                csvs_to_jsonl(inputs, output_path = output, system_instructions=system_instructions)

                if ".jsonl" not in output:
                    raise Exception(f"File {f} is not a .jsonl output!")


        except Exception as e:
            print(e)
            exit

        csv_paths = args[1]
        output_path = args[2]
# run python -m data.training_data_to_jsonl
