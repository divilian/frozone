#!/bin/bash
set -euo pipefail
ensure_gcloud.sh

PROJECT_ID="${PROJECT_ID:-frozone-475719}"
REGION="${REGION:-us-central1}"

if [[ $# -gt 0 ]]; then
  case "$1" in
    running|succeeded|failed|cancelled|all)
      ;; # valid, do nothing
    *)
      echo "Usage: $0 [running|succeeded|failed|cancelled|all]" >&2
      exit 1
      ;;
  esac
fi
if [[ "${1:-}" == "all" ]]; then
  URL="https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${REGION}/tuningJobs"
  EMPTY_MSG="No tuning jobs."
elif [[ "${1:-}" == "succeeded" ]]; then
  URL="https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${REGION}/tuningJobs?filter=state=%22JOB_STATE_SUCCEEDED%22"
  EMPTY_MSG="No jobs succeeded."
elif [[ "${1:-}" == "failed" ]]; then
  URL="https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${REGION}/tuningJobs?filter=state=%22JOB_STATE_FAILED%22"
  EMPTY_MSG="No failed jobs."
elif [[ "${1:-}" == "cancelled" ]]; then
  URL="https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${REGION}/tuningJobs?filter=state=%22JOB_STATE_CANCELLED%22"
  EMPTY_MSG="No cancelled jobs."
else
  URL="https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${REGION}/tuningJobs?filter=state=%22JOB_STATE_RUNNING%22"
  EMPTY_MSG="No running jobs."
fi

resp=$(
  curl -fsS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    "$URL"
)

jq -r --arg msg "$EMPTY_MSG" '(.tuningJobs // []) as $jobs
       | if ($jobs | length) == 0
         then $msg
         else $jobs[] | {name, state, createTime, tunedModelDisplayName}
         end' <<<"$resp"

