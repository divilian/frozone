import csv
from collections import defaultdict
from collections import Counter

import argparse


parser = argparse.ArgumentParser(description="Interactive")
parser.add_argument(
    "-f", "--file",
    type=str,
    default='path/to/file/here',
    help="Input file name"
)
parser.add_argument(
    "-o", "--output",
    type=str,
    default='out.csv',
    help="Output file name"
)

args = parser.parse_args()
FILEPATH = args.file
WRITEPATH = args.output

#order of fields to write to
FIELDS = ["user_message", "ai_response", "dialogue_id", "response_id", "episode_done", "source"]

#identify and group by runs, preserving entire csv row
def process_csv(filepath):
    grouped = defaultdict(list)

    # Read and group
    with open(filepath, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dialogue_id = int(row["dialogue_id"])
            response_id = int(row["response_id"])
            grouped[dialogue_id].append((response_id, row))
            # group[dialogue_id] = [(49, {'user_message': ...}), (50, {'user_message': ...}), ... ]

    # Process in sorted dialogue_id order
    result = {}

    #go through dialogue_id in order
    for dialogue_id in sorted(grouped.keys()):
        dialogue = grouped[dialogue_id]

        # Sort by response_id
        dialogue.sort(key=lambda x: x[0])

        runs = []
        current_run = [dialogue[0][1]]
        prev_id = dialogue[0][0]

        #get all the runs
        for curr_id, row in dialogue[1:]:
            if curr_id == prev_id + 1:
                current_run.append(row)
            else:
                runs.append(current_run)
                current_run = [row]
            prev_id = curr_id

        runs.append(current_run)
        result[dialogue_id] = runs

    return result


def fix_done_labels(processed_data):
    run_lengths = []
    with open(WRITEPATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()

        for dialogue_id, runs in processed_data.items():
            for run in runs:
                # each run is list of dicts
                for i in range(len(run)):
                    row = run[i] #dict

                    # write values the dame in FIELDS order, except with new episode_done
                    if i == len(run)-1:
                        row['episode_done'] = "1"
                    else:
                        row['episode_done'] = "0"

                    writer.writerow(row)


runs = process_csv(FILEPATH)
fix_done_labels(runs)

