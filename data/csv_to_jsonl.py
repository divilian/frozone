import csv
import json
from pathlib import Path
from typing import List, Union
import sys

def base_csv_to_jsonl(csv_files: Union[str, List[str]], output_path: str, system_instructions: str = "INSTRUCTIONS"):

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
    with output_path.open("w", encoding="utf-8-sig") as out_f:
        for ep in episodes:
            json.dump(ep, out_f, ensure_ascii=False)
            out_f.write("\n")

    print(f"Wrote {len(episodes)} episodes to {output_path}")

def single_csv_to_jsonl(csv_files: Union[str, List[str]], output_path: str, system_instructions: str = "INSTRUCTIONS"):

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

        episodes.append({"contents":current_contents})
        current_contents = []

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

def singleWithResponse_csv_to_jsonl(csv_files: Union[str, List[str]],output_path: str,system_instructions: str = "INSTRUCTIONS"):

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

        user_msg = row["user_message"].strip()
        ai_resp = row["ai_response"].strip()

        if toggle:
            cur_msg = system_instructions + "\n" + user_msg
        else:
            cur_msg = cur_msg + "\n" + user_msg

        current_contents.append({"role": "user", "parts": [{"text":cur_msg}]})
        current_contents.append({"role": "model", "parts": [{"text":ai_resp}]})

        episodes.append({"contents":current_contents})
        current_contents = []

        #reset the full message at end of episode
        if row["episode_done"]:
            cur_msg = ""
            toggle = True
        else:
            cur_msg += "\n<RE>: " + ai_resp
            toggle = False
            print(cur_msg)
            
    # Write to JSONL
    output_path = Path(output_path)
    with output_path.open("w", encoding="utf-8-sig") as out_f:
        for ep in episodes:
            json.dump(ep, out_f, ensure_ascii=False)
            out_f.write("\n")

    print(f"Wrote {len(episodes)} episodes to {output_path}")

if __name__ == "__main__":

    args = sys.argv
    try:
        if len(args) == 2 and args[1] == "help":
            printMe = """
To use this converter, you must argue "python csv_to_jsonl.py" followed by these required arguments

"f1.csv,f2.csv,f3.csv,..." which are the csv files you would like to be combined and converted into a single jsonl file. Note that there are no spaces between the file names and all must end in the .csv extension. Also note that these .csv files must have the columns "user_message, ai_response, dialogue_id, response_id, episode_done, issue_labels" to be valid.

"output.jsonl" which is the path and name of the file where you would like the jsonl output from the converter written.

One of "c_, h_, or f_" which refer to which bot's prompt you would like to be used in the training data. The _ is either t or i for the training version of the prompt or the inference version of the prompt. For example, arguing "ct" means 'please use the coolbot_prompt in the training prompts directory' while arguing "fi" means 'please use the frobot_prompt in the inference prompts directory'. 

One of "base, single, singleWithResponse, or singleWithResponseAndProdding" which refer to the diffrent versions of the converter that we have created. Generally, it is best to default to singleWithResponse but below are the diffrences.

    base: This converts it to the default jsonl conversation format where each turn in the conversation is a seperate json object.

    single: This is similar to the base jsonl converter except it intentionally structures the whole conversation into a single json object.

    singleWithResponse: This format is the same as the single converter except that it includes the AI's prior response in the sample.
            """
            print(printMe)
            raise Exception("Thus the usage is python csv_to_jsonl.py f1.csv,f2.csv,f3.csv output.jsonl [ c(i/t) | f(i/t) | h(i/t) ] [ base | single | singleWithResponse ]\n") 
        if len(args) != 5:
            raise Exception("Usage: python csv_to_jsonl.py f1.csv,f2.csv,f3.csv output.jsonl [ c(i/t) | f(i/t) | h(i/t) ] [ base | single | singleWithResponse ]\nUse csv_to_jsonl.py help for more information")

        else:

            inputs = args[1].split(",")
            output = args[2]

            for f in inputs:
                if ".csv" not in f:
                    raise Exception(f"File {f} is not a csv file!")

            if ".jsonl" not in output:
                raise Exception(f"File {f} is not a .jsonl output!")

            #populate system instructions
            #lmao switch statments are for losers the reals ones if ts out
            prompt_file = ""
            if args[3] == 'ci': 
                prompt_file = "inference_prompts/coolbot_prompt_main.txt"

            elif args[3] == "ct":
                prompt_file = "training_prompts/coolbot_prompt_train_main.txt"

            elif args[3] == 'fi':
                prompt_file = "training_prompts/frobot_prompt_main.txt"

            elif args[3] == 'ft':
                prompt_file = "training_prompts/frobot_prompt_train_main.txt"

            elif args[3] == 'hi':
                prompt_file = "training_prompts/hotbot_prompt_main.txt"

            elif args[3] == "hc":
                prompt_file = "training_prompts/hotbot_prompt_train_main.txt"

            else:
                raise Exception(f"Flag {args[3]} is invalid! Must be one of c, f, or h.")

            with open(prompt_file, "r", encoding="utf-8", errors="ignore") as f:
                system_instructions = f.read()
            
            #get out what version of the converter should be used and apply it
            if args[4] == "base":
                base_csv_to_jsonl(inputs, output_path = output, system_instructions=system_instructions)

            elif args[4] == "single":
                single_csv_to_jsonl(inputs, output_path = output, system_instructions=system_instructions)

            elif  args[4] == "singleWithResponse":
                singleWithResponse_csv_to_jsonl(inputs, output_path = output, system_instructions=system_instructions)

            else:
              raise Exception(f"Flag {args[4]} is invalid! Must be one of base, single, or singleWithResponse")

    except Exception as e:
        print(e)
