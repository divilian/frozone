#!/usr/bin/env bash
set -euo pipefail

# json2jsonl.sh
# Usage: ./json2jsonl.sh input.json
# Creates: input.jsonl (must not already exist)

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 INPUT.json" >&2
  exit 2
fi

in="$1"
if [[ ! -r "$in" ]]; then
  echo "Error: cannot read '$in'" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "Error: 'jq' not found. Install jq and retry." >&2
  exit 1
fi

# Derive output name: replace final .json with .jsonl (or just append if no .json)
base="${in%.*}"
ext="${in##*.}"
if [[ "$ext" == "json" ]]; then
  out="${base}.jsonl"
else
  out="${in}.jsonl"
fi

if [[ -e "$out" ]]; then
  echo "Error: output file already exists: $out" >&2
  exit 1
fi

# Transform:
# - Carry over systemInstruction (if present)
# - Split .contents into user/model pairs
# - Only keep valid (user, model) pairs
tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

jq -c '(.systemInstruction // empty) as $sys
| [ .contents[] | {role,parts} ] as $c
| [ range(0; ($c|length))
    | select(. % 2 == 0 and ($c[.].role=="user") and ($c[. + 1].role=="model"))
    | {systemInstruction:$sys, contents:[ $c[.], $c[. + 1] ]}
  ] | .[]' "$in" > "$tmp"

# Sanity check: did we emit anything?
if [[ ! -s "$tmp" ]]; then
  echo "Error: produced empty JSONL. Check that '.contents' has even user/model turns." >&2
  exit 1
fi

mv "$tmp" "$out"
echo "Wrote: $out"

