import csv
import json
from pathlib import Path
from typing import List, Union
import sys

def base_csv_to_jsonl(csv_files: Union[str, List[str]], output_path: str, system_instructions: str = "INSTRUCTIONS" , prompt: str = "PROMPT"):

    if isinstance(csv_files, str):
        csv_files = [csv_files]

    all_rows = []

    # Read all CSVs
    for file in csv_files:
        print(file)
        with open(file, newline='', encoding='utf-8-sig',errors='ignore') as f:
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
    toggle = True
    num_samples = 0

    for row in all_rows:
        # Start new dialogue if needed
        if current_dialogue_id is None:
            current_dialogue_id = row["dialogue_id"]

        # Add user + model turns
        user_msg = row["user_message"].strip()
        ai_resp = row["ai_response"].strip()

        current_contents.append({"role": "user", "parts": [{"text": user_msg}]})
        current_contents.append({"role": "model", "parts": [{"text": ai_resp}]})

        # If this episode is done, finalize
        if row["episode_done"]: 
            current_contents.insert(0,{"role":"user","parts":[{"text": prompt}]})
            episodes.append({
                "systemInstruction": {
                    "role": "system",
                    "parts": [{"text": system_instructions}]
                },
                "contents": current_contents
            })
            num_samples += len(current_contents) // 2
            current_contents = []
            current_dialogue_id = None

    # Write to JSONL
    output_path = Path(output_path)
    with output_path.open("w", encoding="utf-8") as out_f:
        for ep in episodes:
            json.dump(ep, out_f, ensure_ascii=False)
            out_f.write("\n")

    print(f"Wrote {num_samples} samples to {output_path}")

def single_csv_to_jsonl(csv_files: Union[str, List[str]], output_path: str, system_instructions: str = "INSTRUCTIONS" , prompt: str = "PROMPT"):

    if isinstance(csv_files, str):
        csv_files = [csv_files]

    all_rows = []

    # Read all CSVs
    for file in csv_files:
        print(file)
        with open(file, newline='', encoding='utf-8',errors='ignore') as f:
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
            cur_msg = prompt + "\n" + user_msg
        else:
            cur_msg = cur_msg + "\n" + user_msg

        current_contents.append({"role": "user", "parts": [{"text":cur_msg}]})
        current_contents.append({"role": "model", "parts": [{"text":ai_resp}]})
        
        episodes.append({
            "systemInstruction": {"role":"system","parts":[{"text":system_instructions}]},
            "contents":current_contents
        })
        current_contents = []

        #reset the full message at end of episode
        if row["episode_done"]:
            cur_msg = ""
            toggle = True
        else:
            toggle = False
            
    # Write to JSONL
    output_path = Path(output_path)
    with output_path.open("w", encoding="utf-8") as out_f:
        for ep in episodes:
            json.dump(ep, out_f, ensure_ascii=False)
            out_f.write("\n")

    print(f"Wrote {len(episodes)} samples to {output_path}")

def singleWithResponse_csv_to_jsonl(csv_files: Union[str, List[str]],output_path: str,system_instructions: str = "INSTRUCTIONS",prompt: str="PROMPT"):

    if isinstance(csv_files, str):
        csv_files = [csv_files]
    all_rows = []

    # Read all CSVs
    for file in csv_files:
        print(file)
        with open(file, newline='', encoding='utf-8-sig',errors='ignore') as f:
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
            cur_msg = prompt + "\n" + user_msg
        else:
            cur_msg = cur_msg + "\n" + user_msg

        current_contents.append({"role": "user", "parts": [{"text":cur_msg}]})
        current_contents.append({"role": "model", "parts": [{"text":ai_resp}]})

        episodes.append({
            "systemInstruction":{"role":"system","parts":[{"text":system_instructions}]},
            "contents":current_contents
        })
        current_contents = []

        #reset the full message at end of episode
        if row["episode_done"]:
            cur_msg = ""
            toggle = True
        else:
            cur_msg += "\n<RE>: " + ai_resp
            toggle = False
            
    # Write to JSONL
    output_path = Path(output_path)
    with output_path.open("w", encoding="utf-8-sig") as out_f:
        for ep in episodes:
            json.dump(ep, out_f, ensure_ascii=False)
            out_f.write("\n")

    print(f"Wrote {len(episodes)} samples to {output_path}")

if __name__ == "__main__":

    args = sys.argv
    try:
        if len(args) == 2 and args[1] == "help":
            printMe = """
To use this converter, you must argue "python csv_to_jsonl.py" followed by these required arguments

"f1.csv,f2.csv,f3.csv,..." which are the csv files you would like to be combined and converted into a single jsonl file. Note that there are no spaces between the file names and all must end in the .csv extension. Also note that these .csv files must have the columns "user_message, ai_response, dialogue_id, response_id, episode_done, issue_labels" to be valid.

"output.jsonl" which is the path and name of the file where you would like the jsonl output from the converter written.

One of "c_, h_, or f_" which refer to which bot's instructions you would like to be used in the training data. The _ is either t or i for the training version of the instruction or the inference version of the instruction. For example, arguing "ct" means 'please use the coolbot_prompt in the training instructions directory' while arguing "fi" means 'please use the frobot_prompt in the inference instructions directory'. 

One of "base, single, singleWithResponse, or singleWithResponseAndProdding" which refer to the diffrent versions of the converter that we have created. Generally, it is best to default to base but below are the diffrences.

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

            #populate instructions
            #lmao switch statments are for losers the reals ones if ts out
            system_instruct_file = ""
            if args[3] == 'ci': 
                 instruct_file = "/home/garrett/SchoolWork/Frozone/data/inference_instructions/coolbot_instructions_main.txt"

            elif args[3] == "ct":
                 instruct_file = "/home/garrett/SchoolWork/Frozone/data/training_instructions/coolbot_instructions_train_main.txt"

            elif args[3] == 'fi':
                instruct_file = "/home/garrett/SchoolWork/Frozone/data/inference_instructions/frobotbot_instructions_main.txt"

            elif args[3] == 'ft':
                instruct_file = "/home/garrett/SchoolWork/Frozone/data/training_instructions/frobot_instructions_train_main.txt"

            elif args[3] == 'hi':
                instruct_file = "/home/garrett/SchoolWork/Frozone/data/inference_instructions/hotbot_instructions_main.txt"

            elif args[3] == "ht":
                instruct_file = "/home/garrett/SchoolWork/Frozone/data/training_instructions/hotbot_instructions_train_main.txt"
            else:
                raise Exception(f"Flag {args[3]} is invalid! Must be one of c(i/t), f(i/t), or h(i/t).")

            #populate prompt
            prompt_file = ""
            if "c" in args[3]:
                prompt_file = "/home/garrett/SchoolWork/Frozone/data/prompts/coolbot_prompt_main.txt" 

            elif "f" in args[3]:
                prompt_file = "/home/garrett/SchoolWork/Frozone/data/prompts/frobot_prompt_main.txt"

            elif "h" in args[3]:
                prompt_file = "/home/garrett/SchoolWork/Frozone/data/prompts/hotbot_prompt_main.txt"

            else:
                raise Exception(f"Flag {args[3]} is invalid! Must be one of c(i/t), f(i/t), or h(i/t).")

            with open(prompt_file, "r", encoding="utf-8", errors="ignore") as f:
                prompt = f.read()

            with open(instruct_file , "r" , encoding="utf-8" , errors="ignore") as f:
                system_instructions = f.read()
            
            #get out what version of the converter should be used and apply it
            if args[4] == "base":
                base_csv_to_jsonl(inputs, output_path = output, system_instructions=system_instructions,prompt = prompt)

            elif args[4] == "single":
                single_csv_to_jsonl(inputs, output_path = output, system_instructions=system_instructions,prompt = prompt)

            elif  args[4] == "singleWithResponse":
                singleWithResponse_csv_to_jsonl(inputs, output_path = output, system_instructions=system_instructions , prompt = prompt)

            else:
              raise Exception(f"Flag {args[4]} is invalid! Must be one of base, single, or singleWithResponse")

    except Exception as e:
        print(e)
