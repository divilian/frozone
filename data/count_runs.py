"""
python count_runs.py -f path/to/file

Count the number of runs (see this link for a defition of what "runs" means: https://github.com/divilian/frozone/issues/170#issuecomment-3888133721).

Used chatGPT to help write much of this.
"""



import csv
from collections import defaultdict
from collections import Counter

import argparse

DEFAULT_FILEPATH = "coolbot_training/csv_files/coolBotTrainingNoPassCleanedV3.csv"

parser = argparse.ArgumentParser(description="Interactive")
parser.add_argument(
    "-f", "--file",
    type=str,
    default=DEFAULT_FILEPATH,
    help="Input file name"
)

args = parser.parse_args()
FILEPATH = args.file

def process_csv(filepath):
    grouped = defaultdict(list)

    # Read and group
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dialogue_id = int(row["dialogue_id"])
            response_id = int(row["response_id"])
            grouped[dialogue_id].append((response_id, row))

    # Process in sorted dialogue_id order
    result = {}

    for dialogue_id in sorted(grouped.keys()):
        entries = grouped[dialogue_id]

        # Sort by response_id
        entries.sort(key=lambda x: x[0])

        runs = []
        current_run = [entries[0][1]]
        prev_id = entries[0][0]

        for curr_id, row in entries[1:]:
            if curr_id == prev_id + 1:
                current_run.append(row)
            else:
                runs.append(current_run)
                current_run = [row]
            prev_id = curr_id

        runs.append(current_run)
        result[dialogue_id] = runs

    return result

def analyze_runs(processed_data):
    run_lengths = []

    for dialogue_id, runs in processed_data.items():
        for run in runs:
            run_lengths.append(len(run))

    length_counts = Counter(run_lengths)

    return run_lengths, length_counts


processed = process_csv(FILEPATH)

run_lengths, length_counts = analyze_runs(processed)

print("Run length distribution:")
for length in sorted(length_counts):
    print(f"Length {length}: {length_counts[length]} runs")



