#!/usr/bin/env bash
set -euo pipefail
ensure_gcloud.sh

PROJECT_ID="${PROJECT_ID:-frozone-475719}"
REGION="${REGION:-us-central1}"

JOB_ID="${1:-}"
if [[ -z "$JOB_ID" ]]; then
  echo "usage: $(basename "$0") JOB_ID" >&2
  exit 1
fi

JOB_PATH="projects/${PROJECT_ID}/locations/${REGION}/tuningJobs/${JOB_ID}"

curl -fSs \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://${REGION}-aiplatform.googleapis.com/v1/${JOB_PATH}" \
| jq '{tunedModelDisplayName, name, labels, state, outputModel, hp: .supervisedTuningSpec.hyperParameters, exportLastOnly: .supervisedTuningSpec.exportLastCheckpointOnly}'

